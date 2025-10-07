# file: selfaware_ai_bank/utils/markdown_loader.py
import re

def parse_role_markdown(content):
    lines = content.split('\n')
    role = {
        "name": re.search(r"^#\s*(.+)", lines[0]).group(1) if lines else "Unnamed",
        "purpose": next((l for l in lines if l.startswith("Purpose:")), ""),
        "capabilities": [l for l in lines if l.startswith("- ")],
    }
    return role
