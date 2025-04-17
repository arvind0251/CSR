# utils/filters.py
import re

UNWANTED_MESSAGE_REGEX = r"^[\W_]+$|[\/!?\~\\]"

def is_clean_text(text: str) -> bool:
    return not re.match(UNWANTED_MESSAGE_REGEX, text)
