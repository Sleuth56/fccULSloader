"""
FCC Code Definitions Module - FCC Database Code Mappings
=======================================================

Author: Tiran Dagan (Backstop Radio)
Contact: tiran@tirandagan.com
License: MIT License

Description:
-----------
This module provides mappings for various codes used in the FCC Amateur Radio License database.
It translates numeric or letter codes into human-readable descriptions for display purposes.

Dictionaries:
-----------
- applicant_type_code: Maps applicant type codes to their descriptions
  Example: "I" -> "Individual", "B" -> "Amateur Club"

- entity_type: Maps entity type codes to their descriptions
  Example: "L" -> "Licensee or Assignee", "E" -> "Transferee"

Usage:
-----
Import the dictionaries and use them to translate codes:

    from modules import fcc_code_defs
    
    # Translate an applicant type code
    code = "I"
    if code in fcc_code_defs.applicant_type_code:
        description = fcc_code_defs.applicant_type_code[code]
        print(f"{description} ({code})")  # Output: "Individual (I)"
    
    # Translate an entity type code
    code = "L"
    if code in fcc_code_defs.entity_type:
        description = fcc_code_defs.entity_type[code]
        print(f"{description} ({code})")  # Output: "Licensee or Assignee (L)"

References:
----------
These code definitions are based on the FCC's Universal Licensing System (ULS) documentation.
For more information, visit: https://www.fcc.gov/wireless/universal-licensing-system
"""

applicant_type_code = {
    "B": "Amateur Club",
    "C": "Corporation",
    "D": "General Partnership",
    "E": "Limited Partnership",
    "F": "Limited Liability Partnership",
    "G": "Governmental Entity",
    "H": "Other",
    "I": "Individual",
    "J": "Joint Venture",
    "L": "Limited Liability Company",
    "M": "Military Recreation",
    "O": "Consortium",
    "P": "Partnership",
    "R": "RACES",
    "T": "Trust",
    "U": "Unincorporated Association"
}

entity_type = {
    "CE": "Transferee contact",
    "CL": "Licensee Contact",
    "CR": "Assignor or Transferor Contact",
    "CS": "Lessee Contact",
    "E": "Transferee",
    "L": "Licensee or Assignee",
    "O": "Owner",
    "R": "Assignor or Transferor",
    "S": "Lessee"
}

operator_class = {
    "A": "Advanced",
    "E": "Amateur Extra",
    "G": "General",
    "N": "Novice",
    "P": "Technician Plus",
    "T": "Technician"
}

group_code = {
    "B": "Military Recreation",
    "C": "Club",
    "M": "Military Recreation",
    "R": "RACES"
}

region_code = {
    "1": "Northeast",
    "2": "Mid-Atlantic",
    "3": "Southeast",
    "4": "Great Lakes",
    "5": "Central",
    "6": "South Central",
    "7": "Mountain",
    "8": "Pacific",
    "9": "Alaska",
    "0": "Hawaii and Pacific Islands"
}

license_status = {
    "A": "Active",
    "C": "Canceled",
    "E": "Expired",
    "T": "Terminated",
    "P": "Parent Station Canceled",
    "S": "Spectrum Leasing",
    "D": "Discontinued",
    "X": "Term Expired",
    "L": "License Lost"
}

radio_service_code = {
    "HA": "Amateur",
    "HV": "Vanity Amateur"
}

trustee_indicator = {
    "Y": "Yes",
    "N": "No"
}

systematic_call_sign_change = {
    "Y": "Yes",
    "N": "No"
}

vanity_call_sign_change = {
    "Y": "Yes",
    "N": "No"
}

# Dictionary mapping field names to their respective code dictionaries
field_code_mappings = {
    "operator_class": operator_class,
    "group_code": group_code,
    "region_code": region_code,
    "entity_type": entity_type,
    "applicant_type_code": applicant_type_code,
    "license_status": license_status,
    "radio_service_code": radio_service_code,
    "trustee_indicator": trustee_indicator,
    "systematic_call_sign_change": systematic_call_sign_change,
    "vanity_call_sign_change": vanity_call_sign_change
}
