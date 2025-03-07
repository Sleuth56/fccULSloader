# FCC Database Documentation

**Author:** Tiran Dagan (Backstop Radio)  
**Contact:** tiran@tirandagan.com  
**License:** MIT License

This document provides detailed information about the FCC Universal Licensing System (ULS) database tables and fields used in the FCC Loader application.

## Overview

The FCC ULS database contains comprehensive information about amateur radio licenses, including licensee details, license status, and other related information. The database is organized into several tables, each with a specific purpose.

## Common Fields

Several fields appear in multiple tables and have consistent meanings:

- **record_type**: Identifies the type of record (typically matches the table name)
- **unique_system_identifier**: A unique identifier for each license/application in the FCC database
- **uls_file_number**: The ULS file number associated with the application
- **ebf_number**: Electronic batch filing number
- **call_sign**: The amateur radio call sign
- **status_code**: Status code for the record (common values: "A" = Active, "E" = Expired, "T" = Terminated)
- **status_date**: Date when the status was last updated (format: YYYY-MM-DD)

## Table Descriptions

### AM - Amateur License Table

Contains information specific to amateur radio licenses.

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "AM" for this table | "AM" |
| unique_system_identifier | Unique identifier for the license | Integer |
| uls_file_number | ULS file number for the application | Text |
| ebf_number | Electronic batch filing number | Text |
| call_sign | The amateur radio call sign | Text |
| operator_class | License class | "A" = Advanced<br>"E" = Extra<br>"G" = General<br>"N" = Novice<br>"T" = Technician<br>"P" = Technician Plus |
| group_code | Club/Military Recreation/RACES group code | "C" = Club<br>"M" = Military Recreation<br>"R" = RACES |
| region_code | FCC region code | 1-10 (Integer) |
| trustee_call_sign | Call sign of the trustee (for club licenses) | Text |
| trustee_indicator | Indicates if this is a trustee record | "Y" = Yes<br>"N" = No |
| physician_certification | Indicates if physician certification is on file | "Y" = Yes<br>"N" = No |
| ve_signature | Volunteer Examiner signature indicator | "Y" = Yes<br>"N" = No |
| systematic_call_sign_change | Indicates if call sign was systematically changed | "Y" = Yes<br>"N" = No |
| vanity_call_sign_change | Indicates if this is a vanity call sign | "Y" = Yes<br>"N" = No |
| vanity_relationship | Relationship code for vanity call sign | "C" = Club<br>"F" = Former holder<br>"I" = Close relative<br>"L" = Club with consent |
| previous_call_sign | Previous call sign if changed | Text |
| previous_operator_class | Previous operator class if upgraded | Same as operator_class |
| trustee_name | Name of the trustee (for club licenses) | Text |

### EN - Entity Table

Contains information about the licensee (person or organization).

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "EN" for this table | "EN" |
| unique_system_identifier | Unique identifier for the license | Integer |
| uls_file_number | ULS file number for the application | Text |
| ebf_number | Electronic batch filing number | Text |
| call_sign | The amateur radio call sign | Text |
| entity_type | Type of entity | See Entity Type Codes table below |
| licensee_id | Licensee identifier | Text |
| entity_name | Name of the entity (for organizations) | Text |
| first_name | First name (for individuals) | Text |
| mi | Middle initial (for individuals) | Text |
| last_name | Last name (for individuals) | Text |
| suffix | Name suffix | "Jr.", "Sr.", "II", "III", etc. |
| phone | Contact phone number | Text (format: ###-###-####) |
| fax | Fax number | Text (format: ###-###-####) |
| email | Email address | Text |
| street_address | Street address | Text |
| city | City | Text |
| state | Two-letter state code | Two-letter state codes (e.g., "CA", "NY") |
| zip_code | ZIP code | Text (format: #####-####) |
| po_box | Post office box | Text |
| attention_line | Attention line for mail | Text |
| sgin | SGIN code | Text |
| fcc_registration_number | FCC Registration Number (FRN) | 10-digit number |
| applicant_type_code | Type of applicant | See Applicant Type Codes table below |
| applicant_type_code_other | Description if applicant type is "Other" | Text |
| status_code | Status code | "A" = Active<br>"E" = Expired<br>"T" = Terminated |
| status_date | Date when the status was last updated | Date (format: YYYY-MM-DD) |
| _37ghz_license_type | 37 GHz license type | Text |
| linked_unique_sys_id | Linked system identifier | Integer |
| linked_call_sign | Linked call sign | Text |

#### Entity Type Codes

| Code | Description |
|------|-------------|
| CE | Transferee contact |
| CL | Licensee Contact |
| CR | Assignor or Transferor Contact |
| CS | Lessee Contact |
| E | Transferee |
| L | Licensee or Assignee |
| O | Owner |
| R | Assignor or Transferor |
| S | Lessee |

#### Applicant Type Codes

| Code | Description |
|------|-------------|
| B | Amateur Club |
| C | Corporation |
| D | General Partnership |
| E | Limited Partnership |
| F | Limited Liability Partnership |
| G | Governmental Entity |
| H | Other |
| I | Individual |
| J | Joint Venture |
| L | Limited Liability Company |
| M | Military Recreation |
| O | Consortium |
| P | Partnership |
| R | RACES |
| T | Trust |
| U | Unincorporated Association |

### HD - License Header Table

Contains primary license information including status and dates.

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "HD" for this table | "HD" |
| unique_system_identifier | Unique identifier for the license | Integer |
| uls_file_number | ULS file number for the application | Text |
| ebf_number | Electronic batch filing number | Text |
| call_sign | The amateur radio call sign | Text |
| license_status | Status of the license | "A" = Active<br>"E" = Expired<br>"C" = Canceled<br>"T" = Terminated |
| radio_service_code | Radio service code | "HA" = Amateur<br>"HV" = Vanity |
| grant_date | Date the license was granted | Date (format: YYYY-MM-DD) |
| expired_date | Date the license expires | Date (format: YYYY-MM-DD) |
| cancellation_date | Date the license was canceled (if applicable) | Date (format: YYYY-MM-DD) |
| eligibility_rule_num | Eligibility rule number | Text |
| applicant_type_code_reserved | Reserved field for applicant type code | See Applicant Type Codes |
| alien | Indicates if licensee is an alien | "Y" = Yes<br>"N" = No |
| alien_government | Indicates if licensee is a foreign government | "Y" = Yes<br>"N" = No |
| alien_corporation | Indicates if licensee is a foreign corporation | "Y" = Yes<br>"N" = No |
| alien_officer | Indicates if licensee has alien officers | "Y" = Yes<br>"N" = No |
| alien_control | Indicates if licensee is under alien control | "Y" = Yes<br>"N" = No |
| revoked | Indicates if license has been revoked | "Y" = Yes<br>"N" = No |
| convicted | Indicates if licensee has been convicted | "Y" = Yes<br>"N" = No |
| adjudged | Indicates if licensee has been adjudged | "Y" = Yes<br>"N" = No |
| involved_reserved | Reserved field | Text |
| common_carrier | Indicates if licensee is a common carrier | "Y" = Yes<br>"N" = No |
| non_common_carrier | Indicates if licensee is a non-common carrier | "Y" = Yes<br>"N" = No |
| private_comm | Indicates if license is for private communications | "Y" = Yes<br>"N" = No |
| fixed | Indicates if license is for fixed service | "Y" = Yes<br>"N" = No |
| mobile | Indicates if license is for mobile service | "Y" = Yes<br>"N" = No |
| radiolocation | Indicates if license is for radiolocation | "Y" = Yes<br>"N" = No |
| satellite | Indicates if license is for satellite communications | "Y" = Yes<br>"N" = No |
| developmental_or_sta | Indicates if license is developmental or STA | "Y" = Yes<br>"N" = No |
| interconnected_service | Indicates if service is interconnected | "Y" = Yes<br>"N" = No |
| certifier_first_name | First name of certifier | Text |
| certifier_mi | Middle initial of certifier | Text |
| certifier_last_name | Last name of certifier | Text |
| certifier_suffix | Suffix of certifier | Text |
| certifier_title | Title of certifier | Text |
| gender | Gender of licensee | "M" = Male<br>"F" = Female |
| african_american | Indicates if licensee is African American | "Y" = Yes<br>"N" = No |
| native_american | Indicates if licensee is Native American | "Y" = Yes<br>"N" = No |
| hawaiian | Indicates if licensee is Hawaiian | "Y" = Yes<br>"N" = No |
| asian | Indicates if licensee is Asian | "Y" = Yes<br>"N" = No |
| white | Indicates if licensee is White | "Y" = Yes<br>"N" = No |
| ethnicity | Ethnicity of licensee | "H" = Hispanic<br>"N" = Non-Hispanic |
| effective_date | Date the license became effective | Date (format: YYYY-MM-DD) |
| last_action_date | Date of last action on the license | Date (format: YYYY-MM-DD) |
| auction_id | Auction identifier | Integer |
| reg_stat_broad_serv | Regulatory status broadcast service | Text |
| band_manager | Indicates if licensee is a band manager | "Y" = Yes<br>"N" = No |
| type_serv_broad_serv | Type of service broadcast service | Text |
| alien_ruling | Alien ruling | Text |
| licensee_name_change | Indicates if licensee name has changed | "Y" = Yes<br>"N" = No |
| whitespace_ind | White space indicator | "Y" = Yes<br>"N" = No |
| additional_cert_choice | Additional certification choice | Text |
| additional_cert_answer | Additional certification answer | Text |
| discontinuation_ind | Discontinuation indicator | "Y" = Yes<br>"N" = No |
| regulatory_compliance_ind | Regulatory compliance indicator | "Y" = Yes<br>"N" = No |
| eligibility_cert_900 | 900 MHz eligibility certification | "Y" = Yes<br>"N" = No |
| transition_plan_cert_900 | 900 MHz transition plan certification | "Y" = Yes<br>"N" = No |
| return_spectrum_cert_900 | 900 MHz return spectrum certification | "Y" = Yes<br>"N" = No |
| payment_cert_900 | 900 MHz payment certification | "Y" = Yes<br>"N" = No |

### CO - Comments Table

Contains comments associated with licenses.

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "CO" for this table | "CO" |
| unique_system_identifier | Unique identifier for the license | Integer |
| uls_file_number | ULS file number for the application | Text |
| call_sign | The amateur radio call sign | Text |
| comment_date | Date the comment was added | Date (format: YYYY-MM-DD) |
| description | Text of the comment | Text |
| status_code | Status code | "A" = Active<br>"E" = Expired<br>"T" = Terminated |
| status_date | Date when the status was last updated | Date (format: YYYY-MM-DD) |

### HS - History Table

Contains historical information about license actions.

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "HS" for this table | "HS" |
| unique_system_identifier | Unique identifier for the license | Integer |
| uls_file_number | ULS file number for the application | Text |
| call_sign | The amateur radio call sign | Text |
| log_date | Date of the log entry | Date (format: YYYY-MM-DD) |
| code | Code indicating the type of historical action | "LISTU" = License Updated<br>"ADDR" = Address Change<br>"RENEW" = Renewal<br>"GRANT" = Grant<br>"VACAT" = Vacated<br>"MODIF" = Modification |

### LA - License Attachments Table

Contains information about attachments to license applications.

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "LA" for this table | "LA" |
| unique_system_identifier | Unique identifier for the license | Integer |
| call_sign | The amateur radio call sign | Text |
| attachment_code | Code identifying the type of attachment | Text |
| attachment_description | Description of the attachment | Text |
| attachment_date | Date the attachment was added | Date (format: YYYY-MM-DD) |
| attachment_file_name | Filename of the attachment | Text |
| action_performed | Action performed with the attachment | "A" = Added<br>"D" = Deleted<br>"M" = Modified |

### SC - Special Conditions Table

Contains special conditions associated with licenses.

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "SC" for this table | "SC" |
| unique_system_identifier | Unique identifier for the license | Integer |
| uls_file_number | ULS file number for the application | Text |
| ebf_number | Electronic batch filing number | Text |
| call_sign | The amateur radio call sign | Text |
| special_condition_type | Type of special condition | Text |
| special_condition_code | Code for the special condition | Integer |
| status_code | Status code | "A" = Active<br>"E" = Expired<br>"T" = Terminated |
| status_date | Date when the status was last updated | Date (format: YYYY-MM-DD) |

### SF - Special Free Form Conditions Table

Contains free-form special conditions for licenses.

| Field | Description | Possible Values |
|-------|-------------|----------------|
| record_type | Always "SF" for this table | "SF" |
| unique_system_identifier | Unique identifier for the license | Integer |
| uls_file_number | ULS file number for the application | Text |
| ebf_number | Electronic batch filing number | Text |
| call_sign | The amateur radio call sign | Text |
| license_free_form_type | Type of free-form condition | Text |
| unique_license_free_form_identifier | Unique identifier for the free-form condition | Integer |
| sequence_number | Sequence number for the condition | Integer |
| license_free_form_condition | Text of the free-form condition | Text |
| status_code | Status code | "A" = Active<br>"E" = Expired<br>"T" = Terminated |
| status_date | Date when the status was last updated | Date (format: YYYY-MM-DD) |

## Database Relationships

The tables are related primarily through the `unique_system_identifier` field:

- **HD** table contains the primary license information
- **EN** table contains the licensee information
- **AM** table contains amateur-specific license details
- Other tables contain supplementary information like comments, history, attachments, and special conditions

### Relationship Diagram

```
                  +-------+
                  |  HD   |
                  | Table |
                  +---+---+
                      |
                      | unique_system_identifier
                      |
          +-----------+-----------+
          |           |           |
    +-----v----+  +---v---+  +----v----+
    |    EN    |  |  AM   |  |   CO    |
    |  Table   |  | Table |  |  Table  |
    +----------+  +-------+  +---------+
          |           |           |
          |           |           |
    +-----v----+  +---v---+  +----v----+
    |    HS    |  |  LA   |  |   SC    |
    |  Table   |  | Table |  |  Table  |
    +----------+  +-------+  +---------+
                      |
                  +---v---+
                  |  SF   |
                  | Table |
                  +-------+
```

## Optimized Searches

The database is optimized with indexes for efficient searching by:

1. **Call sign** - All tables have indexes on the call_sign field
2. **Name fields** - The EN table has indexes on entity_name, first_name, and last_name
3. **State** - The EN table has an index on the state field
4. **Unique system identifier** - Key tables have indexes on this field for efficient joins

## Common Queries

### Lookup by Call Sign

```sql
SELECT * FROM EN WHERE unique_system_identifier=(
    SELECT unique_system_identifier FROM HD WHERE call_sign=? AND license_status="A"
)
```

### Search by Name

```sql
SELECT EN.*, HD.call_sign 
FROM EN 
JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
WHERE (
    LOWER(EN.entity_name) LIKE LOWER(?) OR 
    LOWER(EN.first_name) LIKE LOWER(?) OR 
    LOWER(EN.mi) LIKE LOWER(?) OR 
    LOWER(EN.last_name) LIKE LOWER(?)
)
AND HD.license_status = 'A'
ORDER BY HD.call_sign
```

### Search by State

```sql
SELECT EN.*, HD.call_sign 
FROM EN 
JOIN HD ON EN.unique_system_identifier = HD.unique_system_identifier
WHERE UPPER(EN.state) = ?
AND HD.license_status = 'A'
ORDER BY HD.call_sign
```

### Get License History

```sql
SELECT HS.* 
FROM HS 
WHERE HS.unique_system_identifier = (
    SELECT unique_system_identifier FROM HD WHERE call_sign = ?
)
ORDER BY HS.log_date DESC
```

## Data Sources

This database is derived from the FCC's Universal Licensing System (ULS) public access files, which can be downloaded from the [FCC website](https://www.fcc.gov/wireless/data/public-access-files-database-downloads).

## References

- [FCC ULS Database Definitions](https://www.fcc.gov/wireless/data/public-access-files-database-downloads)
- [FCC ULS Code Definitions](https://www.fcc.gov/wireless/data/public-access-files-database-downloads)
- [FCC Radio Service Codes](https://www.fcc.gov/wireless/bureau-divisions/technologies-systems-and-innovation-division/rules-regulations-title-47)
- [FCC License Statuses](https://www.fcc.gov/wireless/universal-licensing-system/universal-licensing-system-data-resources) 