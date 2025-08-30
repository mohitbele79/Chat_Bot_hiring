"""
Validation and helper utilities.
"""
import re
from email_validator import validate_email, EmailNotValidError
from typing import List

def validate_email_address(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def validate_phone_number(phone: str) -> bool:
    # Very simple phone check: digits and +, length between 7 and 16
    if not phone:
        return False
    cleaned = re.sub(r'[^\d+]', '', phone)
    return 7 <= len(re.sub(r'\D', '', cleaned)) <= 16

def parse_tech_stack(raw: str) -> List[str]:
    """
    Convert user-entered string into a list of tech names.
    Handles commas, semicolons, spaces, and newlines.
    """
    if not raw:
        return []
    # split on comma, semicolon, newline, or multiple spaces
    parts = re.split(r'[,\n; ]+', raw)
    techs = [p.strip() for p in parts if p.strip()]
    return techs
