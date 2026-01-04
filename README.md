# CS2 Sensitivity Randomizer

Randomize your CS2 sensitivity between 0.7 and 2.1 to improve your aim training. Each run updates your autoexec.cfg and logs the change with a PST timestamp.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/cs2_config_randomizer.git
cd cs2_config_randomizer
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
```

### 3. Create your `.env` file

Copy the example and edit with your CS2 cfg path:

```bash
cp .env.example .env
```

Edit `.env` and set your CS2 config folder location:

```
AUTOEXEC_LOCATION=C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg
```

### 4. Set up your autoexec

Replace the contents of `example_autoexec.cfg` with your own autoexec commands. This file is used as the base template - the script will copy it and add a randomized sensitivity line.

**Important:** Do NOT include a `sensitivity` line in `example_autoexec.cfg` - the script will add it automatically.

## Usage

Run the script to randomize your sensitivity:

```bash
.\env\Scripts\python randomize_sensitivity.py
```

This will:
1. Generate a random sensitivity between 0.7 and 2.1
2. Create `autoexec.cfg` in your CS2 cfg folder with the new sensitivity
3. Log the timestamp, sensitivity, and full config to `logs/sensitivity_log.csv` and `logs/sensitivity_log.json`

## Files

| File | Description |
|------|-------------|
| `randomize_sensitivity.py` | Main script |
| `example_autoexec.cfg` | Your autoexec template (edit this!) |
| `.env` | Your local config (not tracked) |
| `.env.example` | Example config template |
| `logs/` | CSV and JSON logs (not tracked) |

## License

MIT
