import json
import re


def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    # Load the rejected posts
    posts = load_json_file("rejected_posts.json")

    # Initialize lists for separated posts
    llm_rejected = []
    other_rejected = []

    # Pattern to match "Not obviously not Language Model" in the rejection reason
    llm_pattern = re.compile(r"Not obviously not Language Model", re.IGNORECASE)

    # Separate posts
    for post in posts:
        if "RejectedReason" in post and post["RejectedReason"]:
            if llm_pattern.search(post["RejectedReason"]):
                llm_rejected.append(post)
            else:
                other_rejected.append(post)

    # Save the separated posts
    save_json_file(llm_rejected, "llm_rejected_posts.json")
    save_json_file(other_rejected, "other_rejected_posts.json")

    # Print statistics
    print(f"Total posts: {len(posts)}")
    print(f"Posts rejected for 'Not obviously not Language Model': {len(llm_rejected)}")
    print(f"Posts rejected for other reasons: {len(other_rejected)}")


if __name__ == "__main__":
    main()
