"""
CS2 Sensitivity Randomizer
Randomizes sensitivity between 0.7 and 2.1, updates autoexec.cfg, and logs to CSV/JSON.
"""

import os
import random
import json
import csv
from datetime import datetime
from pathlib import Path
import pytz

# Load environment variables from .env file
def load_env():
    env_path = Path(__file__).parent / ".env"
    env_vars = {}
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    return env_vars

def get_pst_timestamp():
    """Get current timestamp in PST timezone."""
    pst = pytz.timezone('America/Los_Angeles')
    return datetime.now(pst).strftime('%Y-%m-%d %H:%M:%S %Z')

def randomize_sensitivity(min_sens=0.7, max_sens=2.1):
    """Generate a random sensitivity value between min and max."""
    return round(random.uniform(min_sens, max_sens), 3)

def read_example_autoexec():
    """Read the example autoexec.cfg file."""
    example_path = Path(__file__).parent / "example_autoexec.cfg"
    with open(example_path, "r") as f:
        return f.read()

def create_autoexec_with_sensitivity(base_content, sensitivity):
    """Add sensitivity command to the autoexec content."""
    sensitivity_line = f'sensitivity "{sensitivity}"'
    
    # Insert sensitivity after the header comment
    lines = base_content.split('\n')
    new_lines = []
    header_found = False
    
    for line in lines:
        new_lines.append(line)
        # Insert sensitivity right after the header section
        if '// =========================' in line and not header_found:
            # Skip to the closing header line
            continue
        if 'CS2 AUTOEXEC' in line:
            header_found = True
        if header_found and '// =========================' in line:
            new_lines.append('')
            new_lines.append('// Sensitivity (randomized)')
            new_lines.append(sensitivity_line)
            header_found = False  # Reset so we don't add again
    
    return '\n'.join(new_lines)

def write_autoexec(content, autoexec_location):
    """Write the autoexec.cfg to the CS2 config folder."""
    autoexec_path = Path(autoexec_location) / "autoexec.cfg"
    with open(autoexec_path, "w") as f:
        f.write(content)
    return autoexec_path

def log_to_csv(timestamp, sensitivity, autoexec_content):
    """Log the change to a CSV file."""
    csv_path = Path(__file__).parent / "logs" / "sensitivity_log.csv"
    file_exists = csv_path.exists()
    
    with open(csv_path, "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp', 'sensitivity', 'autoexec_content'])
        writer.writerow([timestamp, sensitivity, autoexec_content])

def log_to_json(timestamp, sensitivity, autoexec_content):
    """Log the change to a JSON file."""
    json_path = Path(__file__).parent / "logs" / "sensitivity_log.json"
    
    # Load existing data or create new list
    if json_path.exists():
        with open(json_path, "r", encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = []
    
    # Append new entry
    entry = {
        "timestamp": timestamp,
        "sensitivity": sensitivity,
        "autoexec_content": autoexec_content
    }
    data.append(entry)
    
    # Write back
    with open(json_path, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def main():
    print("=" * 50)
    print("CS2 Sensitivity Randomizer")
    print("=" * 50)
    
    # Load environment
    env = load_env()
    autoexec_location = env.get("AUTOEXEC_LOCATION")
    
    if not autoexec_location:
        print("ERROR: AUTOEXEC_LOCATION not found in .env file")
        return
    
    if not Path(autoexec_location).exists():
        print(f"ERROR: Autoexec location does not exist: {autoexec_location}")
        return
    
    # Generate random sensitivity
    sensitivity = randomize_sensitivity()
    print(f"\n🎲 Randomized sensitivity: {sensitivity}")
    
    # Read example and create new autoexec
    base_content = read_example_autoexec()
    new_autoexec = create_autoexec_with_sensitivity(base_content, sensitivity)
    
    # Write to CS2 config folder
    autoexec_path = write_autoexec(new_autoexec, autoexec_location)
    print(f"📁 Written to: {autoexec_path}")
    
    # Get timestamp and log
    timestamp = get_pst_timestamp()
    print(f"🕐 Timestamp (PST): {timestamp}")
    
    log_to_csv(timestamp, sensitivity, new_autoexec)
    print("📊 Logged to sensitivity_log.csv")
    
    log_to_json(timestamp, sensitivity, new_autoexec)
    print("📋 Logged to sensitivity_log.json")
    
    print("\n" + "=" * 50)
    print("✅ Done! Your new autoexec.cfg:")
    print("=" * 50)
    print(new_autoexec)

if __name__ == "__main__":
    main()
