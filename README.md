# Draftable Cleanup Utility

This Python script allows you to list and delete all comparisons from your [Draftable](https://draftable.com/) account using the Draftable API. It supports batch deletion, confirmation prompts, and can be run non-interactively for automation.

## Features
- List all Draftable API comparisons in batches
- Delete comparisons in batches
- Optional confirmation prompt before deletion
- Supports custom API key via command line

## Requirements
- Python 3.6+
- [requests](https://pypi.org/project/requests/)

## Installation
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd draftable-cleanup
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage
Replace `YOUR_DRAFTABLE_API_KEY` in `draftable_cleanup.py` with your actual API key, or provide it via the `--api-key` argument.

Run the script:
```bash
python draftable_cleanup.py
```

### Options
- `--batch-size N` : Number of comparisons to fetch and delete per API request (default: 10)
- `--no-confirm`   : Delete without confirmation prompts (non-interactive mode)
- `--api-key KEY`  : Specify the Draftable API key to use (overrides the value in the script)

### Example: Delete All Comparisons Without Prompt
```bash
python draftable_cleanup.py --batch-size 20 --no-confirm --api-key YOUR_DRAFTABLE_API_KEY
```

### Example: Interactive Deletion
```bash
python draftable_cleanup.py --batch-size 5
```

## Notes
- **Caution:** This script will permanently delete comparisons from your Draftable account. Use with care.
- The script will prompt for confirmation before deleting each batch unless `--no-confirm` is specified.

## License
MIT License 