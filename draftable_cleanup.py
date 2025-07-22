import requests
import argparse
import time
from collections import deque
from datetime import datetime, timedelta

# Replace 'YOUR_DRAFTABLE_API_KEY' with your actual Draftable API key
API_KEY = "YOUR_DRAFTABLE_API_KEY"
API_URL = "https://api.draftable.com/v1/comparisons"
HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json",
}


class RateLimiter:
    """Rate limiter that tracks requests within a sliding window."""

    def __init__(self, max_requests_per_minute):
        self.max_requests = max_requests_per_minute
        self.requests = deque()

    def wait_if_needed(self):
        """Wait if necessary to respect the rate limit."""
        now = datetime.now()

        # Remove requests older than 1 minute
        while self.requests and (now - self.requests[0]) > timedelta(minutes=1):
            self.requests.popleft()

        # If we've hit the rate limit, wait until the oldest request expires
        if len(self.requests) >= self.max_requests:
            sleep_time = (self.requests[0] + timedelta(minutes=1) - now).total_seconds()
            if sleep_time > 0:
                print(f"Rate limit reached. Waiting {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
                # Recursive call to check again after waiting
                return self.wait_if_needed()

        # Add current request timestamp
        self.requests.append(now)


# Global rate limiter instance
rate_limiter = RateLimiter(400)  # Default: 400 requests per minute


def fetch_comparisons_batch(url):
    """Fetch a single batch of comparisons from the given URL."""
    rate_limiter.wait_if_needed()
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Failed to list comparisons: {response.status_code} {response.text}")
        return [], 0
    data = response.json()
    count = data.get("count")
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0
    return data.get("results", []), count


def delete_comparison(identifier):
    """Delete a comparison by its identifier."""
    rate_limiter.wait_if_needed()
    del_url = f"{API_URL}/{identifier}"
    response = requests.delete(del_url, headers=HEADERS)
    if response.status_code == 204:
        print(f"Deleted comparison {identifier}")
    else:
        print(f"Failed to delete {identifier}: {response.status_code} {response.text}")


def main():
    parser = argparse.ArgumentParser(
        description="List and delete all Draftable API comparisons in batches."
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=10,
        help="Number of comparisons to fetch per API request (default: 10)",
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Delete without confirmation prompts (non-interactive mode)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key to be used for Draftable API requests.",
    )
    parser.add_argument(
        "--rate-limit",
        type=int,
        default=400,
        help="Maximum requests per minute (default: 400)",
    )
    parser.add_argument(
        "--delete-id",
        type=str,
        help="Delete a specific comparison by its identifier",
    )
    parser.add_argument(
        "--list-only",
        action="store_true",
        help="List comparisons only, do not delete anything",
    )
    args = parser.parse_args()
    batch_size = args.batch_size
    no_confirm = args.no_confirm
    api_key = args.api_key if args.api_key is not None else API_KEY
    rate_limit = args.rate_limit
    delete_id = args.delete_id
    list_only = args.list_only

    # Update global rate limiter with user-specified rate limit
    global rate_limiter
    rate_limiter = RateLimiter(rate_limit)

    global HEADERS
    HEADERS = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }

    print(f"Rate limit set to {rate_limit} requests per minute")

    # Handle single comparison deletion
    if delete_id:
        print(f"Deleting specific comparison: {delete_id}")
        if not no_confirm:
            confirm = (
                input(
                    f"Are you sure you want to delete comparison {delete_id}? (Y/N): "
                )
                .strip()
                .lower()
            )
            if confirm != "y":
                print("Deletion cancelled. Exiting.")
                return
        delete_comparison(delete_id)
        print("Single comparison deletion completed.")
        return

    total_listed = 0
    batch_num = 1
    offset = 0
    url = f"{API_URL}?limit={batch_size}&offset={offset}"
    print(f"\nFetching batch {batch_num}...")
    comparisons, count = fetch_comparisons_batch(url)

    while url and count > 0:
        print("Count:", count)
        if not comparisons:
            print("No more comparisons to list.")
            break
        print(f"Found {len(comparisons)} comparisons in this batch.")
        print("Comparisons:")
        for comp in comparisons:
            identifier = comp.get("identifier", "N/A")
            created = comp.get("creation_time", "N/A")
            print(f"Identifier: {identifier} | Created: {created}")
            total_listed += 1

        if list_only:
            print(f"Listed {len(comparisons)} comparisons in this batch.")
            batch_num += 1
            offset += batch_size
            url = f"{API_URL}?limit={batch_size}&offset={offset}"
            confirm = (
                input(
                    "\nList next batch? (Y/N): "
                )
                .strip()
                .lower()
            )
            if confirm != "y":
                print("Exiting.")
                break
            else:
                print("Listing next batch.")
                comparisons, count = fetch_comparisons_batch(url)
                continue

        if not no_confirm:
            confirm = (
                input(
                    "\nAre you sure you want to delete this batch of comparisons? (Y/N): "
                )
                .strip()
                .lower()
            )
            if confirm != "y":
                print("Deletion cancelled. Exiting.")
                break
        else:
            print("Auto-confirm enabled: deleting this batch without prompt.")
        for comp in comparisons:
            identifier = comp.get("identifier")
            if identifier:
                delete_comparison(identifier)
            else:
                print(f"No identifier found in: {comp}")
        batch_num += 1
        comparisons, count = fetch_comparisons_batch(url)

    if list_only:
        print(f"\nDone. Total comparisons listed: {total_listed}")
    else:
        print(f"\nDone. Total comparisons deleted: {total_listed}")


if __name__ == "__main__":
    main()
