"""
FCC Database Module - FCC Amateur Radio License Database Operations
==================================================================

Author: Tiran Dagan (Backstop Radio)
Contact: tiran@tirandagan.com
License: MIT License

Description:
-----------
This module provides a comprehensive interface for interacting with the FCC Amateur Radio
License database. It encapsulates all database operations including creation, querying,
optimization, and maintenance.

Classes:
-------
FCCDatabase: Main class that handles all database operations

    Methods:
    -------
    Database Setup and Maintenance:
    - __init__(db_path): Initialize with database path
    - ensure_db_directory(): Ensure database directory exists
    - create_connection(): Create a connection to the SQLite database
    - create_tables(tables_to_process): Create database tables
    - create_indexes(tables_to_process): Create indexes for tables
    - disable_indexes(tables_to_process): Disable indexes for tables
    - enable_indexes(tables_to_process): Enable indexes for tables
    - get_column_count(table): Get the number of columns in a table
    - database_exists(): Check if the database file exists
    
    Database Optimization:
    - compact_database(): Compact the database to reduce file size
    - optimize_database(): Remove unused tables and columns
    - rebuild_indexes(): Rebuild all indexes to improve search performance
    
    Data Queries:
    - get_record_by_call_sign(call_sign): Get record by call sign
    - search_records_by_name(name): Search records by name
    - search_records_by_state(state): Search records by state
    - search_records_by_name_and_state(name, state): Search by name and state
    
    Display Functions:
    - display_record(record): Display a record in a formatted way (static method)
    - display_verbose_record(record): Display all fields of a record

Usage:
-----
1. Create an instance of FCCDatabase with the path to the database file:
   db = FCCDatabase('/path/to/database.db')

2. Use the methods to interact with the database:
   - Query data: db.get_record_by_call_sign('W1AW')
   - Optimize: db.optimize_database()
   - Rebuild indexes: db.rebuild_indexes()

Dependencies:
------------
- sqlite3: SQLite database interface
- modules.schemas: Table schemas, index definitions, and column counts
- modules.fcc_code_defs: FCC code definitions for display
- modules.filesystemtools: File system operations
"""

import sqlite3
import re
import os
import logging
from modules.schemas import table_schemas, index_schemas, column_counts
from modules import fcc_code_defs
from modules.filesystemtools import ensure_directory, file_exists

class FCCDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.ensure_db_directory()

    def ensure_db_directory(self):
        """
        Ensure the database directory exists.
        """
        ensure_directory('db', self.db_path)

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path, uri=False)
            return conn
        except sqlite3.Error as e:
            print(f"Error creating connection to SQLite: {e}")
            return None

    def create_tables(self, tables_to_process):
        conn = self.create_connection()
        if conn:
            try:
                c = conn.cursor()
                for table in tables_to_process:
                    c.execute(table_schemas[table])
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error creating table: {e}")
            finally:
                conn.close()

    def insert_batch_records(self, table, records):
        """
        Insert batch records into the database, handling duplicates by first deleting
        records with the same unique_system_identifier.
        
        Args:
            table (str): The table to insert records into
            records (list): A list of records to insert
        """
        if not records:
            return
        
        conn = self.create_connection()
        if conn:
            try:
                c = conn.cursor()
                
                # For tables with unique_system_identifier, handle duplicates
                if table in ["AM", "CO", "EN", "HD", "HS", "SC", "SF"]:
                    # Extract unique_system_identifiers from the records
                    # The position of unique_system_identifier is 1 in all tables
                    unique_ids = [record[1] for record in records if len(record) > 1]
                    
                    # Create chunks of 500 IDs to avoid SQLite parameter limit
                    chunk_size = 500
                    for i in range(0, len(unique_ids), chunk_size):
                        chunk = unique_ids[i:i + chunk_size]
                        placeholders = ','.join(['?'] * len(chunk))
                        if placeholders:  # Only execute if we have IDs
                            delete_sql = f"DELETE FROM {table} WHERE unique_system_identifier IN ({placeholders})"
                            c.execute(delete_sql, chunk)
                
                # Now insert the new records
                insert_sql = f"INSERT INTO {table} VALUES ({','.join(['?'] * self.get_column_count(table))})"
                c.executemany(insert_sql, records)
                conn.commit()
                
            except sqlite3.Error as e:
                print(f"Error inserting records into {table}: {e}")
            finally:
                conn.close()

    def create_indexes(self, tables_to_process):
        conn = self.create_connection()
        if conn:
            try:
                c = conn.cursor()
                for table in tables_to_process:
                    for index_sql in index_schemas[table]:
                        c.execute(index_sql)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error creating index: {e}")
            finally:
                conn.close()

    def disable_indexes(self, tables_to_process):
        """
        Disable indexes for the specified tables to improve data loading performance.
        
        Args:
            tables_to_process: List of tables to disable indexes for
        """
        conn = self.create_connection()
        if conn:
            try:
                c = conn.cursor()
                # Count total indexes to drop
                total_indexes = sum(len(index_schemas[table]) for table in tables_to_process)
                logging.info(f"Disabling {total_indexes} indexes for {len(tables_to_process)} tables to improve loading performance...")
                
                for table in tables_to_process:
                    for index_sql in index_schemas[table]:
                        match = re.search(r'CREATE INDEX IF NOT EXISTS (.*?) ON', index_sql)
                        if match:
                            index_name = match.group(1)
                            c.execute(f"DROP INDEX IF EXISTS {index_name};")
                conn.commit()
                logging.info("All indexes disabled successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error disabling indexes: {e}")
            finally:
                conn.close()

    def enable_indexes(self, tables_to_process):
        """
        Enable indexes for the specified tables.
        
        Args:
            tables_to_process: List of tables to enable indexes for
        """
        conn = self.create_connection()
        if conn:
            try:
                c = conn.cursor()
                # Count total indexes to create
                total_indexes = sum(len(index_schemas[table]) for table in tables_to_process)
                logging.info(f"Creating {total_indexes} indexes for {len(tables_to_process)} tables...")
                
                for table in tables_to_process:
                    for index_sql in index_schemas[table]:
                        c.execute(index_sql)
                conn.commit()
                logging.info("All indexes created successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error enabling indexes: {e}")
            finally:
                conn.close()

    def get_column_count(self, table):
        return column_counts.get(table, 0)

    def get_record_by_call_sign(self, call_sign):
        """
        Retrieves the record from the EN table using the given call sign.
        
        Args:
            call_sign (str): The call sign to look up.
        
        Returns:
            dict: The record from the EN table if found, otherwise None.
        """
        query = """
        SELECT * FROM EN WHERE unique_system_identifier=(
            SELECT unique_system_identifier FROM HD WHERE call_sign=? AND license_status="A"
        )
        """
        
        try:
            conn = self.create_connection()
            if not conn:
                return None
                
            cursor = conn.cursor()
            cursor.execute(query, (call_sign,))
            record = cursor.fetchone()
            if record:
                field_names = [description[0] for description in cursor.description]
                result_dict = dict(zip(field_names, record))
            else:
                result_dict = None
            conn.close()
            return result_dict
        except sqlite3.Error as e:
            print(f"Error retrieving record: {e}")
            return None

    def compact_database(self):
        """
        Compacts the SQLite database to reduce its file size.
        
        Returns:
            bool: True if compaction was successful, False otherwise.
        """
        try:
            conn = self.create_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            
            # Run VACUUM command to rebuild the database file
            cursor.execute("VACUUM")
            
            conn.commit()
            conn.close()
            print(f"Database compacted successfully: {self.db_path}")
            return True
        except sqlite3.Error as e:
            print(f"Error compacting database: {e}")
            return False

    def optimize_database(self):
        """
        Optimizes the database by:
        1. Removing tables that are not used in the query operations
        2. Removing unused columns from the active tables
        
        Only keeps the essential columns in EN and HD tables which are used for call sign lookups.
        
        Returns:
            bool: True if optimization was successful, False otherwise.
        """
        try:
            conn = self.create_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            
            # Get all tables in the database
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            all_tables = [table[0] for table in cursor.fetchall()]
            
            # Tables used in our queries
            used_tables = ['EN', 'HD']
            
            # Tables to be removed
            tables_to_remove = [table for table in all_tables if table not in used_tables and not table.startswith('sqlite_')]
            
            # Remove unused tables
            for table in tables_to_remove:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
                print(f"Removed unused table: {table}")
            
            # Define essential columns for each table
            essential_columns = {
                'HD': ['unique_system_identifier', 'call_sign', 'license_status'],
                'EN': ['*']  # Keep all columns in EN as we're selecting all of them in the query
            }
            
            # Optimize columns in each used table
            for table in used_tables:
                if table in essential_columns:
                    # Get current table schema
                    cursor.execute(f"PRAGMA table_info({table})")
                    all_columns = [col[1] for col in cursor.fetchall()]
                    
                    # If we're keeping all columns, skip this table
                    if essential_columns[table] == ['*']:
                        print(f"Keeping all columns in table {table}")
                        continue
                    
                    # Determine which columns to keep
                    columns_to_keep = [col for col in all_columns if col in essential_columns[table]]
                    
                    if len(columns_to_keep) < len(all_columns):
                        # Create a new table with only the essential columns
                        columns_str = ', '.join(columns_to_keep)
                        cursor.execute(f"CREATE TABLE {table}_new AS SELECT {columns_str} FROM {table}")
                        
                        # Drop the old table and rename the new one
                        cursor.execute(f"DROP TABLE {table}")
                        cursor.execute(f"ALTER TABLE {table}_new RENAME TO {table}")
                        
                        removed_columns = len(all_columns) - len(columns_to_keep)
                        print(f"Optimized table {table}: removed {removed_columns} unused columns")
            
            conn.commit()
            
            # Compact the database after optimization
            cursor.execute("VACUUM")
            
            conn.close()
            print(f"Database optimized successfully: {self.db_path}")
            if not tables_to_remove:
                print("No unused tables found to remove.")
            else:
                print(f"Removed {len(tables_to_remove)} unused tables.")
            return True
        except sqlite3.Error as e:
            print(f"Error optimizing database: {e}")
            return False

    def search_records_by_name(self, name):
        """
        Searches for records in the EN table where the entity name contains the given name.
        Performs a case-insensitive wildcard search to match partial names in any position.
        
        Args:
            name (str): The name to search for.
        
        Returns:
            list: A list of dictionaries containing the matching records.
        """
        # Create search pattern for wildcard search
        search_pattern = f"%{name}%"
        
        # Optimize the query to use indexes more effectively
        # First, get the unique_system_identifier values that match our criteria
        query = """
        WITH matching_ids AS (
            SELECT DISTINCT EN.unique_system_identifier
            FROM EN 
            JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
            WHERE (
                LOWER(EN.entity_name) LIKE LOWER(?) OR 
                LOWER(EN.first_name) LIKE LOWER(?) OR 
                LOWER(EN.mi) LIKE LOWER(?) OR 
                LOWER(EN.last_name) LIKE LOWER(?)
            )
            AND HD.license_status = 'A'
        )
        SELECT EN.*, HD.call_sign 
        FROM EN 
        JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
        JOIN matching_ids ON EN.unique_system_identifier = matching_ids.unique_system_identifier
        ORDER BY HD.call_sign
        """
        
        try:
            conn = self.create_connection()
            if not conn:
                return []
                
            # Enable query optimization
            conn.execute("PRAGMA optimize")
            cursor = conn.cursor()
            cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            records = cursor.fetchall()
            
            result_list = []
            if records:
                field_names = [description[0] for description in cursor.description]
                
                # Use a set to track unique combinations of unique_system_identifier and call_sign
                seen_records = set()
                
                for record in records:
                    result_dict = dict(zip(field_names, record))
                    
                    # Create a unique key for this record
                    unique_key = (result_dict['unique_system_identifier'], result_dict['call_sign'])
                    
                    # Only add this record if we haven't seen it before
                    if unique_key not in seen_records:
                        seen_records.add(unique_key)
                        result_list.append(result_dict)
            
            conn.close()
            return result_list
        except sqlite3.Error as e:
            print(f"Error searching records by name: {e}")
            return []

    def search_records_by_state(self, state):
        """
        Searches for records in the EN table where the state matches the given state code.
        
        Args:
            state (str): The two-letter state code to search for.
        
        Returns:
            list: A list of dictionaries containing the matching records.
        """
        # Convert state to uppercase for consistency
        state = state.upper()
        
        # Optimize the query to use indexes more effectively
        query = """
        WITH matching_ids AS (
            SELECT DISTINCT EN.unique_system_identifier
            FROM EN 
            JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
            WHERE UPPER(EN.state) = ?
            AND HD.license_status = 'A'
        )
        SELECT EN.*, HD.call_sign 
        FROM EN 
        JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
        JOIN matching_ids ON EN.unique_system_identifier = matching_ids.unique_system_identifier
        ORDER BY HD.call_sign
        """
        
        try:
            conn = self.create_connection()
            if not conn:
                return []
                
            # Enable query optimization
            conn.execute("PRAGMA optimize")
            cursor = conn.cursor()
            cursor.execute(query, (state,))
            records = cursor.fetchall()
            
            result_list = []
            if records:
                field_names = [description[0] for description in cursor.description]
                
                # Use a set to track unique combinations of unique_system_identifier and call_sign
                seen_records = set()
                
                for record in records:
                    result_dict = dict(zip(field_names, record))
                    
                    # Create a unique key for this record
                    unique_key = (result_dict['unique_system_identifier'], result_dict['call_sign'])
                    
                    # Only add this record if we haven't seen it before
                    if unique_key not in seen_records:
                        seen_records.add(unique_key)
                        result_list.append(result_dict)
            
            conn.close()
            return result_list
        except sqlite3.Error as e:
            print(f"Error searching records by state: {e}")
            return []

    def search_records_by_name_and_state(self, name, state=None):
        """
        Searches for records in the EN table where the entity name contains the given name
        and optionally filters by state.
        Performs a case-insensitive wildcard search to match partial names in any position.
        
        Args:
            name (str): The name to search for.
            state (str, optional): The two-letter state code to filter by.
        
        Returns:
            list: A list of dictionaries containing the matching records.
        """
        # Create search pattern for wildcard search
        search_pattern = f"%{name}%"
        
        # Base query for name search - optimize with CTE
        query = """
        WITH matching_ids AS (
            SELECT DISTINCT EN.unique_system_identifier
            FROM EN 
            JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
            WHERE (
                LOWER(EN.entity_name) LIKE LOWER(?) OR 
                LOWER(EN.first_name) LIKE LOWER(?) OR 
                LOWER(EN.mi) LIKE LOWER(?) OR 
                LOWER(EN.last_name) LIKE LOWER(?)
            )
        """
        
        # Add state filter if provided
        params = [search_pattern, search_pattern, search_pattern, search_pattern]
        if state:
            state = state.upper()
            query += "AND UPPER(EN.state) = ? "
            params.append(state)
        
        # Add license status filter and close the CTE
        query += """
            AND HD.license_status = 'A'
        )
        SELECT EN.*, HD.call_sign 
        FROM EN 
        JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
        JOIN matching_ids ON EN.unique_system_identifier = matching_ids.unique_system_identifier
        ORDER BY HD.call_sign
        """
        
        try:
            conn = self.create_connection()
            if not conn:
                return []
                
            # Enable query optimization
            conn.execute("PRAGMA optimize")
            cursor = conn.cursor()
            cursor.execute(query, params)
            records = cursor.fetchall()
            
            result_list = []
            if records:
                field_names = [description[0] for description in cursor.description]
                
                # Use a set to track unique combinations of unique_system_identifier and call_sign
                seen_records = set()
                
                for record in records:
                    result_dict = dict(zip(field_names, record))
                    
                    # Create a unique key for this record
                    unique_key = (result_dict['unique_system_identifier'], result_dict['call_sign'])
                    
                    # Only add this record if we haven't seen it before
                    if unique_key not in seen_records:
                        seen_records.add(unique_key)
                        result_list.append(result_dict)
            
            conn.close()
            return result_list
        except sqlite3.Error as e:
            print(f"Error searching records by name and state: {e}")
            return []

    def rebuild_indexes(self):
        """
        Rebuilds all indexes in the database to improve search performance.
        
        Returns:
            bool: True if rebuilding indexes was successful, False otherwise.
        """
        try:
            conn = self.create_connection()
            if not conn:
                return False
                
            cursor = conn.cursor()
            
            # First, analyze the database
            cursor.execute("ANALYZE")
            
            # Rebuild indexes for EN table
            print("Rebuilding indexes for EN table...")
            cursor.execute("REINDEX idx_EN_unique_sys_id")
            cursor.execute("REINDEX idx_EN_entity_name")
            cursor.execute("REINDEX idx_EN_first_name")
            cursor.execute("REINDEX idx_EN_last_name")
            cursor.execute("REINDEX idx_EN_state")
            
            # Try to create new optimized indexes if they don't exist
            try:
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_EN_state_unique_sys_id ON EN (state, unique_system_identifier)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_EN_name_search ON EN (entity_name, first_name, last_name)")
                print("Created new optimized indexes for name and state searches.")
            except sqlite3.Error as e:
                print(f"Note: Could not create new indexes: {e}")
            
            # Rebuild indexes for HD table
            print("Rebuilding indexes for HD table...")
            cursor.execute("REINDEX idx_HD_call_sign")
            cursor.execute("REINDEX idx_HD_unique_sys_id")
            
            # Try to create new optimized index if it doesn't exist
            try:
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_HD_license_status ON HD (license_status)")
                print("Created new optimized index for license status.")
            except sqlite3.Error as e:
                print(f"Note: Could not create license status index: {e}")
            
            # Optimize the database
            cursor.execute("PRAGMA optimize")
            
            conn.commit()
            conn.close()
            print(f"Indexes rebuilt successfully: {self.db_path}")
            return True
        except sqlite3.Error as e:
            print(f"Error rebuilding indexes: {e}")
            return False

    def database_exists(self):
        """
        Check if the database file exists.
        
        Returns:
            bool: True if the database file exists, False otherwise
        """
        return file_exists(self.db_path)
    
    def remove_inactive_records(self):
        """
        Remove all inactive license records from the database.
        
        This removes records from the HD table where license_status is not 'A',
        and also removes related records from other tables.
        
        The user is prompted to confirm before records are deleted.
        """
        conn = self.create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # First, identify all inactive records in the HD table
                logging.info("Identifying inactive records...")
                cursor.execute("CREATE TEMPORARY TABLE temp_inactive_records AS SELECT unique_system_identifier, call_sign FROM HD WHERE license_status != 'A'")
                
                # Get count of inactive records
                cursor.execute("SELECT COUNT(*) FROM temp_inactive_records")
                inactive_count = cursor.fetchone()[0]
                
                if inactive_count == 0:
                    logging.info("No inactive records found in the database")
                    print("No inactive records found in the database. Nothing to delete.")
                    cursor.execute("DROP TABLE temp_inactive_records")
                    return
                
                # Get a sample of call signs to show the user
                cursor.execute("SELECT call_sign FROM temp_inactive_records LIMIT 10")
                sample_calls = [row[0] for row in cursor.fetchall() if row[0]]
                sample_text = ", ".join(sample_calls) if sample_calls else "N/A"
                
                # Ask for confirmation
                print(f"\nWARNING: This will delete {inactive_count} inactive license records from the database.")
                print(f"Sample of call signs to be deleted: {sample_text}")
                print("\nThis action cannot be undone. Related records in other tables will also be deleted.")
                
                confirmation = input("\nAre you sure you want to continue? (yes/no): ").strip().lower()
                
                if confirmation != "yes":
                    print("Operation cancelled. No records were deleted.")
                    cursor.execute("DROP TABLE temp_inactive_records")
                    return
                
                # Start a transaction
                conn.execute("BEGIN TRANSACTION")
                
                # Delete related records from other tables
                for table in ["AM", "CO", "EN", "HS", "LA", "SC", "SF"]:
                    try:
                        # Check if the table exists
                        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
                        if cursor.fetchone():
                            logging.info(f"Removing inactive records from {table} table...")
                            cursor.execute(f"""
                                DELETE FROM {table} 
                                WHERE unique_system_identifier IN (
                                    SELECT unique_system_identifier FROM temp_inactive_records
                                )
                            """)
                            deleted = cursor.rowcount
                            logging.info(f"Removed {deleted} records from {table} table")
                            print(f"Removed {deleted} records from {table} table")
                    except sqlite3.Error as e:
                        logging.error(f"Error removing inactive records from {table}: {e}")
                
                # Delete inactive records from HD table
                logging.info("Removing inactive records from HD table...")
                cursor.execute("""
                    DELETE FROM HD 
                    WHERE unique_system_identifier IN (
                        SELECT unique_system_identifier FROM temp_inactive_records
                    )
                """)
                deleted = cursor.rowcount
                logging.info(f"Removed {deleted} records from HD table")
                print(f"Removed {deleted} records from HD table")
                
                # Drop the temporary table
                cursor.execute("DROP TABLE temp_inactive_records")
                
                # Commit the transaction
                conn.commit()
                
                # Vacuum the database to reclaim space
                logging.info("Vacuuming database to reclaim space...")
                print("Vacuuming database to reclaim space...")
                conn.execute("VACUUM")
                
                logging.info("Inactive records removal completed")
                print("\nInactive records have been successfully removed from the database.")
                
            except sqlite3.Error as e:
                logging.error(f"Database error during inactive records removal: {e}")
                conn.rollback()
                print(f"Error: {e}")
            finally:
                conn.close()
        else:
            logging.error("Could not connect to the database")
            print("Error: Could not connect to the database")

    @staticmethod
    def display_record(record):
        """
        Displays a record in a formatted way.
        
        Args:
            record (dict): The record to display.
        """
        # Display call sign first if available
        if 'call_sign' in record:
            print(f"Call Sign: {record['call_sign']}")
        
        # Display name information
        if record.get('entity_name'):
            print(f"Entity Name: {record['entity_name']}")
        else:
            name_parts = []
            if record.get('first_name'):
                name_parts.append(record['first_name'])
            if record.get('mi'):
                name_parts.append(record['mi'])
            if record.get('last_name'):
                name_parts.append(record['last_name'])
            if name_parts:
                print(f"Name: {' '.join(name_parts)}")
        
        # Display other important fields
        important_fields = ['unique_system_identifier', 'entity_type', 'applicant_type_code', 'city', 'state', 'zip_code']
        for field in important_fields:
            if field in record and record[field]:
                if field == 'entity_type' and record[field] in fcc_code_defs.entity_type:
                    print(f"Entity Type: {fcc_code_defs.entity_type[record[field]]} ({record[field]})")
                elif field == 'applicant_type_code' and record[field] in fcc_code_defs.applicant_type_code:
                    print(f"Applicant Type: {fcc_code_defs.applicant_type_code[record[field]]} ({record[field]})")
                else:
                    print(f"{field.replace('_', ' ').title()}: {record[field]}")
        
        print("-" * 40)  # Separator between records

    def display_verbose_record(self, record):
        """
        Displays all fields of a record.
        
        Args:
            record (dict): The record to display.
        """
        for f in record:
            if record[f]:
                if f == 'entity_type' and record[f] in fcc_code_defs.entity_type:
                    print(f"{f}: {fcc_code_defs.entity_type[record[f]]} ({record[f]})")
                elif f == 'applicant_type_code' and record[f] in fcc_code_defs.applicant_type_code:
                    print(f"{f}: {fcc_code_defs.applicant_type_code[record[f]]} ({record[f]})")
                else:
                    print(f"{f}: {record[f]}")
        print("-" * 40)  # Separator between records
