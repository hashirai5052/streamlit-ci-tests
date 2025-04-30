# codee/__init__.py
from .codee import (
    contains_open_house,
    extract_phone_numbers,
    normalize_phone,
    clean_name,
    escape_special_characters,
    ensure_string,
    transform_record,
    # …etc
)
# In test_codee.py
from codee.codee import close_geometry  # Import specific functions
import codee
  # Import the whole module