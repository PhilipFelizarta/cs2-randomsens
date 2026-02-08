"""
CS2 Sensitivity Randomizer
Randomizes sensitivity between 0.7 and 2.1, updates autoexec.cfg, and logs to CSV/JSON.
"""

import argparse
import os
import random
import json
import csv
from datetime import datetime
from pathlib import Path
import pytz

# Config file paths
CONFIG_DIR = Path(__file__).parent / "config"
SETTINGS_FILE = CONFIG_DIR / "settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "main_sensitivity": 1.0,
    "lower_bound": 0.7,
    "upper_bound": 2.1
}

def load_settings():
    """Load settings from JSON file."""
    CONFIG_DIR.mkdir(exist_ok=True)
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """Save settings to JSON file."""
    CONFIG_DIR.mkdir(exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)

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

def randomize_sensitivity(min_sens=None, max_sens=None):
    """Generate a random sensitivity value between min and max."""
    settings = load_settings()
    if min_sens is None:
        min_sens = settings["lower_bound"]
    if max_sens is None:
        max_sens = settings["upper_bound"]
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

def apply_sensitivity(sensitivity, label="randomized"):
    """Apply a sensitivity value to the autoexec and log it."""
    env = load_env()
    autoexec_location = env.get("AUTOEXEC_LOCATION")
    
    if not autoexec_location:
        print("ERROR: AUTOEXEC_LOCATION not found in .env file")
        return False
    
    if not Path(autoexec_location).exists():
        print(f"ERROR: Autoexec location does not exist: {autoexec_location}")
        return False
    
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
    print(f"✅ Done! Sensitivity ({label}): {sensitivity}")
    print("=" * 50)
    return True

def cmd_set_main_sens(value):
    """Set the main/favorite sensitivity."""
    settings = load_settings()
    settings["main_sensitivity"] = float(value)
    save_settings(settings)
    print(f"✅ Main sensitivity set to: {value}")

def cmd_main():
    """Apply the main/favorite sensitivity."""
    settings = load_settings()
    sensitivity = settings["main_sensitivity"]
    print("=" * 50)
    print("CS2 Sensitivity - Using Main Sensitivity")
    print("=" * 50)
    print(f"\n⭐ Main sensitivity: {sensitivity}")
    apply_sensitivity(sensitivity, label="main")

def cmd_show_random():
    """Show the random sensitivity range."""
    settings = load_settings()
    print("=" * 50)
    print("Random Sensitivity Range")
    print("=" * 50)
    print(f"  Lower bound: {settings['lower_bound']}")
    print(f"  Upper bound: {settings['upper_bound']}")

def cmd_set_lower(value):
    """Set the lower bound for random sensitivity."""
    settings = load_settings()
    settings["lower_bound"] = float(value)
    save_settings(settings)
    print(f"✅ Lower bound set to: {value}")

def cmd_set_upper(value):
    """Set the upper bound for random sensitivity."""
    settings = load_settings()
    settings["upper_bound"] = float(value)
    save_settings(settings)
    print(f"✅ Upper bound set to: {value}")

def cmd_random():
    """Apply a random sensitivity (default behavior)."""
    print("=" * 50)
    print("CS2 Sensitivity Randomizer")
    print("=" * 50)
    
    sensitivity = randomize_sensitivity()
    print(f"\n🎲 Randomized sensitivity: {sensitivity}")
    apply_sensitivity(sensitivity, label="randomized")

def main():
    parser = argparse.ArgumentParser(
        description="CS2 Sensitivity Randomizer - Randomize or set your CS2 sensitivity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                  Randomize sensitivity
  python main.py --main           Use your favorite sensitivity
  python main.py --set-main-sens 1.5   Set favorite sensitivity to 1.5
  python main.py --show-random    Show random sensitivity range
  python main.py --set-lower 0.5  Set lower bound to 0.5
  python main.py --set-upper 2.5  Set upper bound to 2.5
        """
    )
    
    parser.add_argument("--set-main-sens", type=float, metavar="VALUE",
                        help="Set your favorite/main sensitivity")
    parser.add_argument("--main", action="store_true",
                        help="Use your favorite sensitivity instead of random")
    parser.add_argument("--show-random", action="store_true",
                        help="Show the random sensitivity range")
    parser.add_argument("--set-lower", type=float, metavar="VALUE",
                        help="Set the lower bound for random sensitivity")
    parser.add_argument("--set-upper", type=float, metavar="VALUE",
                        help="Set the upper bound for random sensitivity")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.set_main_sens is not None:
        cmd_set_main_sens(args.set_main_sens)
    elif args.main:
        cmd_main()
    elif args.show_random:
        cmd_show_random()
    elif args.set_lower is not None:
        cmd_set_lower(args.set_lower)
    elif args.set_upper is not None:
        cmd_set_upper(args.set_upper)
    else:
        # Default: randomize
        cmd_random()

if __name__ == "__main__":
    main()
