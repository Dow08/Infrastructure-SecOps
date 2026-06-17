#!/usr/bin/env python3
# Soul Shield: A custom security scanner and redactor to prevent secret leaks
# in the automated VPS / Hermes soul backup pipeline.

import os
import re
import sqlite3
import sys

# Secret detection patterns
PATTERNS = {
    "Anthropic API Key": re.compile(r"sk-ant-[0-9a-zA-Z_\-]{80,}"),
    "OpenAI API Key": re.compile(r"sk-(?:proj-)?[a-zA-Z0-9_\-]{40,}"),
    "Google Gemini API Key": re.compile(r"AIzaSy[a-zA-Z0-9_\-]{33}"),
    "GitHub PAT": re.compile(r"gh[p|o|u|r]_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_\-]{82}"),
    "Slack Token": re.compile(r"xox[b|p|p|o|r]-[0-9]{12}-[a-zA-Z0-9]{12,24}"),
    "Generic Assignment Secret": re.compile(r"(?i)(api_key|client_secret|private_key|token|auth_token)\s*[:=]\s*['\"]([a-zA-Z0-9_\-]{20,})['\"]"),
}

SOUL_DIR = "/root/VPS_Jarod_AI_et_OSINT/soul"

def scan_and_redact_text_file(filepath):
    """Scans and automatically redacts secrets from text files."""
    if not os.path.exists(filepath):
        return True, 0

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        original_content = content
        redactions = 0

        for key, pattern in PATTERNS.items():
            matches = pattern.findall(content)
            if matches:
                for match in matches:
                    # If it's a tuple from generic regex, extract the secret part
                    secret = match[1] if isinstance(match, tuple) else match
                    if "[REDACTED_BY_SOUL_SHIELD]" in secret:
                        continue
                    
                    print(f"[SHIELD] Warning: Detected active {key} in {os.path.basename(filepath)}! Redacting...")
                    content = content.replace(secret, f"[REDACTED_BY_SOUL_SHIELD_{key.upper().replace(' ', '_')}]")
                    redactions += 1

        if redactions > 0:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[SHIELD] Redacted {redactions} secrets in {filepath}.")

        return True, redactions
    except Exception as e:
        print(f"[SHIELD] Error scanning text file {filepath}: {e}")
        return False, 0

def scan_sqlite_db(db_path):
    """Scans SQLite databases for leak hazards and sanitizes them."""
    if not os.path.exists(db_path):
        return True, 0

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # We search inside messages table (content column) which is the primary risk area
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages';")
        if not cursor.fetchone():
            conn.close()
            return True, 0

        cursor.execute("SELECT id, content FROM messages WHERE content IS NOT NULL;")
        rows = cursor.fetchall()
        
        redactions = 0
        for row_id, content in rows:
            modified_content = content
            row_updated = False
            
            for key, pattern in PATTERNS.items():
                matches = pattern.findall(content)
                if matches:
                    for match in matches:
                        secret = match[1] if isinstance(match, tuple) else match
                        if "[REDACTED_BY_SOUL_SHIELD]" in secret:
                            continue
                        
                        print(f"[SHIELD] Hazard: Found {key} in message ID {row_id}! Redacting from database copy...")
                        modified_content = modified_content.replace(secret, f"[REDACTED_BY_SOUL_SHIELD_{key.upper().replace(' ', '_')}]")
                        row_updated = True
                        redactions += 1
            
            if row_updated:
                cursor.execute("UPDATE messages SET content = ? WHERE id = ?;", (modified_content, row_id))
        
        if redactions > 0:
            conn.commit()
            print(f"[SHIELD] Sanitized {redactions} database leak hazards successfully.")
        
        conn.close()
        return True, redactions
    except Exception as e:
        print(f"[SHIELD] Error scanning database {db_path}: {e}")
        return False, 0

def main():
    print("[SHIELD] Launching pre-commit security verification...")
    
    total_redactions = 0
    success = True
    
    # Text files to scan
    text_files = [
        os.path.join(SOUL_DIR, "config.yaml"),
        os.path.join(SOUL_DIR, "memories/USER.md"),
        os.path.join(SOUL_DIR, "memories/MEMORY.md"),
    ]
    
    for text_file in text_files:
        ok, count = scan_and_redact_text_file(text_file)
        if not ok:
            success = False
        total_redactions += count
        
    # DB to scan
    db_path = os.path.join(SOUL_DIR, "state.db")
    ok, count = scan_sqlite_db(db_path)
    if not ok:
        success = False
    total_redactions += count
    
    print(f"[SHIELD] Verification finished. Success: {success}, Redactions made: {total_redactions}")
    
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
