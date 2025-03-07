"""
FCC ULS Downloader and Loader
Author: Tiran Dagan
Contact: tiran@tirandagan.com

Description: Configuration for table schemas, index statements, and column counts.
"""

table_schemas = {
    "AM": """
    CREATE TABLE IF NOT EXISTS AM (
        record_type TEXT,
        unique_system_identifier INTEGER,
        uls_file_number TEXT,
        ebf_number TEXT,
        call_sign TEXT,
        operator_class TEXT,
        group_code TEXT,
        region_code INTEGER,
        trustee_call_sign TEXT,
        trustee_indicator TEXT,
        physician_certification TEXT,
        ve_signature TEXT,
        systematic_call_sign_change TEXT,
        vanity_call_sign_change TEXT,
        vanity_relationship TEXT,
        previous_call_sign TEXT,
        previous_operator_class TEXT,
        trustee_name TEXT
    );
    """,
    "CO": """
    CREATE TABLE IF NOT EXISTS CO (
        record_type TEXT,
        unique_system_identifier INTEGER,
        uls_file_number TEXT,
        call_sign TEXT,
        comment_date TEXT,
        description TEXT,
        status_code TEXT,
        status_date TEXT
    );
    """,
    "EN": """
    CREATE TABLE IF NOT EXISTS EN (
        record_type TEXT,
        unique_system_identifier INTEGER,
        uls_file_number TEXT,
        ebf_number TEXT,
        call_sign TEXT,
        entity_type TEXT,
        licensee_id TEXT,
        entity_name TEXT,
        first_name TEXT,
        mi TEXT,
        last_name TEXT,
        suffix TEXT,
        phone TEXT,
        fax TEXT,
        email TEXT,
        street_address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        po_box TEXT,
        attention_line TEXT,
        sgin TEXT,
        fcc_registration_number TEXT,
        applicant_type_code TEXT,
        applicant_type_code_other TEXT,
        status_code TEXT,
        status_date TEXT,
        _37ghz_license_type TEXT,
        linked_unique_sys_id INTEGER,
        linked_call_sign TEXT
    );
    """,
    "HD": """
    CREATE TABLE IF NOT EXISTS HD (
        record_type TEXT,
        unique_system_identifier INTEGER,
        uls_file_number TEXT,
        ebf_number TEXT,
        call_sign TEXT,
        license_status TEXT,
        radio_service_code TEXT,
        grant_date TEXT,
        expired_date TEXT,
        cancellation_date TEXT,
        eligibility_rule_num TEXT,
        applicant_type_code_reserved TEXT,
        alien TEXT,
        alien_government TEXT,
        alien_corporation TEXT,
        alien_officer TEXT,
        alien_control TEXT,
        revoked TEXT,
        convicted TEXT,
        adjudged TEXT,
        involved_reserved TEXT,
        common_carrier TEXT,
        non_common_carrier TEXT,
        private_comm TEXT,
        fixed TEXT,
        mobile TEXT,
        radiolocation TEXT,
        satellite TEXT,
        developmental_or_sta TEXT,
        interconnected_service TEXT,
        certifier_first_name TEXT,
        certifier_mi TEXT,
        certifier_last_name TEXT,
        certifier_suffix TEXT,
        certifier_title TEXT,
        gender TEXT,
        african_american TEXT,
        native_american TEXT,
        hawaiian TEXT,
        asian TEXT,
        white TEXT,
        ethnicity TEXT,
        effective_date TEXT,
        last_action_date TEXT,
        auction_id INTEGER,
        reg_stat_broad_serv TEXT,
        band_manager TEXT,
        type_serv_broad_serv TEXT,
        alien_ruling TEXT,
        licensee_name_change TEXT,
        whitespace_ind TEXT,
        additional_cert_choice TEXT,
        additional_cert_answer TEXT,
        discontinuation_ind TEXT,
        regulatory_compliance_ind TEXT,
        eligibility_cert_900 TEXT,
        transition_plan_cert_900 TEXT,
        return_spectrum_cert_900 TEXT,
        payment_cert_900 TEXT
    );
    """,
    "HS": """
    CREATE TABLE IF NOT EXISTS HS (
        record_type TEXT,
        unique_system_identifier INTEGER,
        uls_file_number TEXT,
        call_sign TEXT,
        log_date TEXT,
        code TEXT
    );
    """,
    "LA": """
    CREATE TABLE IF NOT EXISTS LA (
        record_type TEXT,
        unique_system_identifier INTEGER,
        call_sign TEXT,
        attachment_code TEXT,
        attachment_description TEXT,
        attachment_date TEXT,
        attachment_file_name TEXT,
        action_performed TEXT
    );
    """,
    "SC": """
    CREATE TABLE IF NOT EXISTS SC (
        record_type TEXT,
        unique_system_identifier INTEGER,
        uls_file_number TEXT,
        ebf_number TEXT,
        call_sign TEXT,
        special_condition_type TEXT,
        special_condition_code INTEGER,
        status_code TEXT,
        status_date TEXT
    );
    """,
    "SF": """
    CREATE TABLE IF NOT EXISTS SF (
        record_type TEXT,
        unique_system_identifier INTEGER,
        uls_file_number TEXT,
        ebf_number TEXT,
        call_sign TEXT,
        license_free_form_type TEXT,
        unique_license_free_form_identifier INTEGER,
        sequence_number INTEGER,
        license_free_form_condition TEXT,
        status_code TEXT,
        status_date TEXT
    );
    """
}

index_schemas = {
    "AM": ["CREATE INDEX IF NOT EXISTS idx_AM_call_sign ON AM (call_sign);",
           "CREATE INDEX IF NOT EXISTS idx_AM_unique_sys_id ON AM (unique_system_identifier);"],
    "CO": ["CREATE INDEX IF NOT EXISTS idx_CO_call_sign ON CO (call_sign);"],
    "EN": ["CREATE INDEX IF NOT EXISTS idx_EN_call_sign ON EN (call_sign);",
           "CREATE INDEX IF NOT EXISTS idx_EN_unique_sys_id ON EN (unique_system_identifier);",
           "CREATE INDEX IF NOT EXISTS idx_EN_entity_name ON EN (entity_name);",
           "CREATE INDEX IF NOT EXISTS idx_EN_first_name ON EN (first_name);",
           "CREATE INDEX IF NOT EXISTS idx_EN_last_name ON EN (last_name);",
           "CREATE INDEX IF NOT EXISTS idx_EN_state ON EN (state);",
           "CREATE INDEX IF NOT EXISTS idx_EN_state_unique_sys_id ON EN (state, unique_system_identifier);",
           "CREATE INDEX IF NOT EXISTS idx_EN_name_search ON EN (entity_name, first_name, last_name);"],
    "HD": ["CREATE INDEX IF NOT EXISTS idx_HD_call_sign ON HD (call_sign,license_status);",
           "CREATE INDEX IF NOT EXISTS idx_HD_unique_sys_id ON HD (unique_system_identifier);",
           "CREATE INDEX IF NOT EXISTS idx_HD_license_status ON HD (license_status);"],
    "HS": ["CREATE INDEX IF NOT EXISTS idx_HS_call_sign ON HS (call_sign);"],
    "LA": ["CREATE INDEX IF NOT EXISTS idx_LA_call_sign ON LA (call_sign);"],
    "SC": ["CREATE INDEX IF NOT EXISTS idx_SC_call_sign ON SC (call_sign);"],
    "SF": ["CREATE INDEX IF NOT EXISTS idx_SF_call_sign ON SF (call_sign);"]
}

column_counts = {
    "AM": 18,
    "CO": 8,
    "EN": 30,
    "HD": 59,
    "HS": 6,
    "LA": 8,
    "SC": 9,
    "SF": 11
}

field_names = {
    "AM": [
        "record_type", "unique_system_identifier", "uls_file_number", "ebf_number", "call_sign",
        "operator_class", "group_code", "region_code", "trustee_call_sign", "trustee_indicator",
        "physician_certification", "ve_signature", "systematic_call_sign_change", "vanity_call_sign_change",
        "vanity_relationship", "previous_call_sign", "previous_operator_class", "trustee_name"
    ],
    "CO": [
        "record_type", "unique_system_identifier", "uls_file_number", "call_sign", "comment_date",
        "description", "status_code", "status_date"
    ],
    "EN": [
        "record_type", "unique_system_identifier", "uls_file_number", "ebf_number", "call_sign",
        "entity_type", "licensee_id", "entity_name", "first_name", "mi", "last_name", "suffix", "phone", "fax",
        "email", "street_address", "city", "state", "zip_code", "po_box", "attention_line", "sgin",
        "fcc_registration_number", "applicant_type_code", "applicant_type_code_other", "status_code",
        "status_date", "_37ghz_license_type", "linked_unique_sys_id", "linked_call_sign"
    ],
    "HD": [
        "record_type", "unique_system_identifier", "uls_file_number", "ebf_number", "call_sign",
        "license_status", "radio_service_code", "grant_date", "expired_date", "cancellation_date",
        "eligibility_rule_num", "applicant_type_code_reserved", "alien", "alien_government", "alien_corporation", 
        "alien_officer", "alien_control", "revoked", "convicted", "adjudged", "involved_reserved",
        "common_carrier", "non_common_carrier", "private_comm", "fixed", "mobile", "radiolocation",
        "satellite", "developmental_or_sta", "interconnected_service", "certifier_first_name", "certifier_mi",
        "certifier_last_name", "certifier_suffix", "certifier_title", "gender", "african_american",
        "native_american", "hawaiian", "asian", "white", "ethnicity", "effective_date", "last_action_date",
        "auction_id", "reg_stat_broad_serv", "band_manager", "type_serv_broad_serv", "alien_ruling",
        "licensee_name_change", "whitespace_ind", "additional_cert_choice", "additional_cert_answer",
        "discontinuation_ind", "regulatory_compliance_ind", "eligibility_cert_900", "transition_plan_cert_900",
        "return_spectrum_cert_900", "payment_cert_900"
    ],
    "HS": [
        "record_type", "unique_system_identifier", "uls_file_number", "call_sign", "log_date", "code"
    ],
    "LA": [
        "record_type", "unique_system_identifier", "call_sign", "attachment_code", "attachment_description",
        "attachment_date", "attachment_file_name", "action_performed"
    ],
    "SC": [
        "record_type", "unique_system_identifier", "uls_file_number", "ebf_number", "call_sign",
        "special_condition_type", "special_condition_code", "status_code", "status_date"
    ],
    "SF": [
        "record_type", "unique_system_identifier", "uls_file_number", "ebf_number", "call_sign",
        "license_free_form_type", "unique_license_free_form_identifier", "sequence_number",
        "license_free_form_condition", "status_code", "status_date"
    ]
}
