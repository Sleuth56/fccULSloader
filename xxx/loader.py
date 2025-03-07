"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Module to handle loading data into the database.
"""

import os
import logging
from datetime import datetime
from modules.database import FCCDatabase
from multiprocessing import Pool, cpu_count
from modules.schemas import field_names
from modules.progress import create_record_progress_bar

BATCH_SIZE = 10000

def parse_file(file_path, expected_fields, table):
    """
    Parse the file and handle multiline records. Convert date fields for specific tables.
    """
    def convert_date(date_str):
        if date_str == '':
            return ''
        else:
            try:
                return datetime.strptime(date_str, '%m/%d/%Y').strftime('%Y-%m-%d')
            except ValueError:
                return date_str

    date_indices = [i for i, col in enumerate(field_names[table]) if 'date' in col.lower()]

    record = []
    with open(file_path, 'r') as file:
        for line in file:
            stripped_line = line.rstrip('\n')
            if '|' in stripped_line:
                fields = stripped_line.split('|')
                if record:
                    record[-1] += '\n' + fields[0]
                    record.extend(fields[1:])
                else:
                    record.extend(fields)

                while len(record) >= expected_fields:
                    for idx in date_indices:
                        record[idx] = convert_date(record[idx])
                    yield record[:expected_fields]
                    record = record[expected_fields:]
            else:
                if record:
                    record[-1] += '\n' + stripped_line
    
    if record:
        if len(record) < expected_fields:
            record = pad_record(record, expected_fields)
        for idx in date_indices:
            record[idx] = convert_date(record[idx])
        yield record[:expected_fields]

def pad_record(record, expected_length):
    """
    Pad the record to ensure it has the expected length.
    """
    return record + [''] * (expected_length - len(record))

def load_data_batch(args):
    """
    Insert batch records into the database.
    """
    db_path, table, records = args
    db = FCCDatabase(db_path)
    db.insert_batch_records(table, records)

def load_data_single_threaded(db, file_path, table, total_records):
    """
    Load data into the database using single-threaded approach.
    """
    records = []
    processed_records = 0

    expected_length = db.get_column_count(table)

    conn = db.create_connection()
    with conn:
        conn.execute("PRAGMA synchronous = OFF;")
        conn.execute("PRAGMA journal_mode = MEMORY;")
        conn.execute("PRAGMA cache_size = 1000000;")
        conn.execute("BEGIN TRANSACTION;")

        # Create custom progress bar
        pbar = create_record_progress_bar(
            total_records=total_records,
            desc=f"Loading {table} data",
            unit="records"
        )

        for record in parse_file(file_path, expected_length, table):
            if len(record) == expected_length:
                records.append(record)
                processed_records += 1
            else:
                if len(record) < expected_length:
                    record = pad_record(record, expected_length)
                    records.append(record)
                    processed_records += 1
                else:
                    logging.warning(f"Skipping invalid record in {table}: {record}")

            if len(records) >= BATCH_SIZE:
                db.insert_batch_records(table, records)
                records = []
                pbar.update(BATCH_SIZE)

        if records:  # Insert any remaining records
            db.insert_batch_records(table, records)
            pbar.update(len(records))

        pbar.close()
        conn.execute("COMMIT;")

def load_data_multithreaded(db, file_path, table, total_records):
    """
    Load data into the database using multithreaded approach.
    """
    records = list(parse_file(file_path, db.get_column_count(table), table))
    total_records = len(records)
    expected_length = db.get_column_count(table)

    padded_records = []
    for record in records:
        if len(record) <= expected_length:
            padded_records.append(pad_record(record, expected_length))
        else:
            logging.warning(f"Skipping invalid record in {table}: {record}")

    batches = [padded_records[i:i + BATCH_SIZE] for i in range(0, len(padded_records), BATCH_SIZE)]

    conn = db.create_connection()
    with conn:
        conn.execute("PRAGMA synchronous = OFF;")
        conn.execute("PRAGMA journal_mode = MEMORY;")
        conn.execute("PRAGMA cache_size = 1000000;")
        conn.execute("BEGIN TRANSACTION;")

        # Create custom progress bar
        pbar = create_record_progress_bar(
            total_records=total_records,
            desc=f"Loading {table} data",
            unit="records"
        )

        with Pool(cpu_count()) as pool:
            for batch in pool.imap_unordered(load_data_batch, [(db.db_path, table, batch) for batch in batches]):
                pbar.update(len(batch))

        pbar.close()
        conn.execute("COMMIT;")

def parse_counts_file(counts_file_path):
    """
    Parse the counts file to get the expected number of records for each table.
    If the file doesn't exist, return an empty dictionary.
    """
    counts = {}
    try:
        with open(counts_file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    count, path = parts
                    table_name = os.path.basename(path).split('.')[0]
                    counts[table_name] = int(count)
        return counts
    except FileNotFoundError:
        logging.warning(f"Counts file not found at {counts_file_path}. Will proceed without record counts.")
        return counts

def load_all_data(db, extract_path, use_multithreading, tables_to_process):
    """
    Load all data from the extracted files into the database.
    """
    counts_file_path = os.path.join(extract_path, "counts")
    counts = parse_counts_file(counts_file_path)

    for table in tables_to_process:
        file_path = os.path.join(extract_path, f"{table}.dat")
        if os.path.exists(file_path):
            # If we don't have a count, estimate it from file size
            if table not in counts or counts[table] == 0:
                file_size = os.path.getsize(file_path)
                # Rough estimate: assume average record is 100 bytes
                estimated_records = max(1, file_size // 100)
                counts[table] = estimated_records
                logging.info(f"Estimated {estimated_records} records for {table} based on file size.")
            
            total_records = counts.get(table, 0)
            if use_multithreading:
                load_data_multithreaded(db, file_path, table, total_records)
            else:
                load_data_single_threaded(db, file_path, table, total_records)
        else:
            logging.warning(f"{file_path} not found in the extracted files.")
