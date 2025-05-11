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
