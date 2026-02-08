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
.\env\Scripts\python main.py
```

### Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Randomize sensitivity (default) |
| `python main.py --main` | Use your favorite/main sensitivity |
| `python main.py --set-main-sens 1.5` | Set your favorite sensitivity |
| `python main.py --show-random` | Show the random sensitivity range |
| `python main.py --set-lower 0.5` | Set the lower bound for random |
| `python main.py --set-upper 2.5` | Set the upper bound for random |
| `python main.py --help` | Show all available commands |

### What it does

1. Generates a random sensitivity (or uses your main sens with `--main`)
2. Creates `autoexec.cfg` in your CS2 cfg folder with the new sensitivity
3. Logs the timestamp, sensitivity, and full config to `logs/`

## Files

| File | Description |
|------|-------------|
| `main.py` | Main script |
| `example_autoexec.cfg` | Your autoexec template (edit this!) |
| `.env` | Your local config (not tracked) |
| `.env.example` | Example config template |
| `config/` | Saved settings like main sens, bounds (not tracked) |
| `logs/` | CSV and JSON logs (not tracked) |

## License

MIT
