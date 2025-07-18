import requests
import argparse

# Replace 'YOUR_DRAFTABLE_API_KEY' with your actual Draftable API key
API_KEY = "YOUR_DRAFTABLE_API_KEY"
API_URL = "https://api.draftable.com/v1/comparisons"
HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json",
}


def fetch_comparisons_batch(url):
    """Fetch a single batch of comparisons from the given URL."""
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
    args = parser.parse_args()
    batch_size = args.batch_size
    no_confirm = args.no_confirm
    api_key = args.api_key if args.api_key is not None else API_KEY
    global HEADERS
    HEADERS = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
    }

    url = f"{API_URL}?limit={batch_size}"
    total_deleted = 0
    batch_num = 1
    print(f"\nFetching batch {batch_num}...")
    comparisons, count = fetch_comparisons_batch(url)

    while url and count > 0:
        print("Count:", count)
        if not comparisons:
            print("No more comparisons to delete.")
            break
        print(f"Found {len(comparisons)} comparisons in this batch.")
        print("Comparisons:")
        for comp in comparisons:
            identifier = comp.get("identifier", "N/A")
            created = comp.get("creation_time", "N/A")
            print(f"Identifier: {identifier} | Created: {created}")
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
                total_deleted += 1
            else:
                print(f"No identifier found in: {comp}")
        batch_num += 1
        comparisons, count = fetch_comparisons_batch(url)
    print(f"\nDone. Total comparisons deleted: {total_deleted}")


if __name__ == "__main__":
    main()
