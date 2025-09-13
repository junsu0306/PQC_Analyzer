import json
import re
from config.settings import CLUES_JSON_PATH
from src.utils.logger import logger

class CodeScanner:
    def __init__(self, clues_path=CLUES_JSON_PATH):
        try:
            with open(clues_path, 'r', encoding='utf-8') as f:
                self.clues = json.load(f)
            logger.info(f"Successfully loaded {len(self.clues)} clues from {clues_path}.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load or parse clues file: {e}")
            self.clues = []

    def scan_code(self, code: str) -> list[dict]:
        """Scans the code for predefined clues and returns a list of findings."""
        found_clues = []
        for clue in self.clues:
            pattern = clue.get("pattern")
            if not pattern:
                continue

            found = False
            if clue["type"] == "keyword":
                if re.search(r'\b' + re.escape(pattern) + r'\b', code, re.IGNORECASE):
                    found = True
            
            elif clue["type"] == "magic_number":
                code_normalized = ''.join(code.split()).lower()
                if pattern.lower() in code_normalized:
                    found = True
            
            if found:
                # 같은 단서가 여러 번 발견되어도 한 번만 추가하도록
                clue_to_add = {
                    "id": clue["clue_id"],
                    "type": clue["type"],
                    "matched_pattern": pattern
                }
                if clue_to_add not in found_clues:
                    found_clues.append(clue_to_add)
        
        return found_clues

scanner_instance = CodeScanner()