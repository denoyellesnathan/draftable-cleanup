# Draftable Cleanup Utility

This Python script allows you to list and delete all comparisons from your [Draftable](https://draftable.com/) account using the Draftable API. It supports batch deletion, confirmation prompts, rate limiting, and can be run non-interactively for automation.

## Features
- List all Draftable API comparisons in batches
- Delete comparisons in batches
- **Rate limiting** with configurable requests per minute (default: 400)
- Optional confirmation prompt before deletion
- Supports custom API key via command line
- Non-interactive mode for automation

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
- `--rate-limit N` : Maximum requests per minute (default: 400)
- `--delete-id ID` : Delete a specific comparison by its identifier
- `--list-only`    : List comparisons only, do not delete anything

### Rate Limiting
The script includes a built-in rate limiter that prevents exceeding API rate limits:
- **Default**: 400 requests per minute
- **Configurable**: Use `--rate-limit` to set custom limits
- **Automatic**: The script will automatically wait when the rate limit is reached
- **Sliding window**: Uses a 1-minute sliding window for accurate rate limiting

### Example: List All Comparisons Without Deleting
```bash
# List all comparisons with default batch size
python draftable_cleanup.py --list-only --api-key YOUR_DRAFTABLE_API_KEY

# List with larger batch size for faster listing
python draftable_cleanup.py --list-only --batch-size 50 --api-key YOUR_DRAFTABLE_API_KEY
```

### Example: Delete All Comparisons Without Prompt
```bash
python draftable_cleanup.py --batch-size 20 --no-confirm --api-key YOUR_DRAFTABLE_API_KEY
```

### Example: Delete a Specific Comparison
```bash
# Delete a single comparison with confirmation
python draftable_cleanup.py --delete-id ABC123 --api-key YOUR_DRAFTABLE_API_KEY

# Delete a single comparison without confirmation
python draftable_cleanup.py --delete-id ABC123 --no-confirm --api-key YOUR_DRAFTABLE_API_KEY
```

### Example: Custom Rate Limiting
```bash
# Set rate limit to 200 requests per minute
python draftable_cleanup.py --rate-limit 200 --api-key YOUR_DRAFTABLE_API_KEY

# Conservative rate limiting for sensitive APIs
python draftable_cleanup.py --rate-limit 100 --batch-size 5 --no-confirm
```

### Example: Interactive Deletion with Rate Limiting
```bash
$ python draftable_cleanup.py --api-key YOUR_DRAFTABLE_API_KEY

Rate limit set to 400 requests per minute
Fetching batch 1...
Count: 84868
Found 10 comparisons in this batch.
Comparisons:
Identifier: OVmCpFNH | Created: 2025-07-18T15:49:43.415564Z
Identifier: OmmbzCDC | Created: 2025-07-18T13:33:35.322469Z
Identifier: NTlCzADK | Created: 2025-07-18T12:15:22.123456Z
...

Are you sure you want to delete this batch of comparisons? (Y/N): y
Deleted comparison OVmCpFNH
Deleted comparison OmmbzCDC
Deleted comparison NTlCzADK
...
```

### Example: Rate Limit in Action
When the rate limit is reached, you'll see messages like:
```
Rate limit reached. Waiting 12.34 seconds...
Deleted comparison ABC123
```

## Notes
- **Caution:** This script will permanently delete comparisons from your Draftable account. Use with care.
- The script will prompt for confirmation before deleting each batch unless `--no-confirm` is specified.
- **Rate Limiting**: The rate limiter uses a sliding window approach, ensuring you never exceed the specified requests per minute limit.
- **API Limits**: Check your Draftable API documentation for actual rate limits. The default 400 requests/minute should work for most accounts.

## License
MIT License 