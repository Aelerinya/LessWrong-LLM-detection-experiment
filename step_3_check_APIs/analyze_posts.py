import json
import os
import time
import argparse
from typing import Dict, List, Any
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from tqdm import tqdm
from dotenv import load_dotenv
from enum import Enum
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
from copyleaks.models.submit.ai_detection_document import NaturalLanguageDocument


# Load environment variables from .env file
load_dotenv()


class DetectorAPI(Enum):
    SAPLING = "sapling"
    UNDETECTABLE = "undetectable"
    COPYLEAKS = "copyleaks"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Analyze posts using AI detection APIs"
    )
    parser.add_argument(
        "--api",
        choices=[api.value for api in DetectorAPI],
        default=os.getenv("DETECTOR_API", "sapling").lower(),
        help="Select which API to use for detection",
    )
    return parser.parse_args()


# Configuration
args = parse_args()
DETECTOR_API = args.api
SAPLING_API_KEY = os.getenv("SAPLING_API_KEY")
UNDETECTABLE_API_KEY = os.getenv("UNDETECTABLE_API_KEY")
COPYLEAKS_EMAIL = os.getenv("COPYLEAKS_EMAIL")
COPYLEAKS_API_KEY = os.getenv("COPYLEAKS_API_KEY")

if DETECTOR_API == DetectorAPI.SAPLING.value and not SAPLING_API_KEY:
    raise ValueError("Please set the SAPLING_API_KEY environment variable in .env file")
elif DETECTOR_API == DetectorAPI.UNDETECTABLE.value and not UNDETECTABLE_API_KEY:
    raise ValueError(
        "Please set the UNDETECTABLE_API_KEY environment variable in .env file"
    )
elif DETECTOR_API == DetectorAPI.COPYLEAKS.value and not (
    COPYLEAKS_EMAIL and COPYLEAKS_API_KEY
):
    raise ValueError(
        "Please set both COPYLEAKS_EMAIL and COPYLEAKS_API_KEY environment variables in .env file"
    )

# API URLs
SAPLING_API_URL = "https://api.sapling.ai/api/v1/aidetect"
UNDETECTABLE_API_URL = "https://ai-detect.undetectable.ai/detect"

# Copyleaks authentication token
copyleaks_auth_token = None
if DETECTOR_API == DetectorAPI.COPYLEAKS.value:
    try:
        copyleaks_auth_token = Copyleaks.login(COPYLEAKS_EMAIL, COPYLEAKS_API_KEY)
    except CommandError as ce:
        response = ce.get_response()
        raise ValueError(f"Failed to authenticate with Copyleaks: {response.content}")

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds


def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    backoff_max=120,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        backoff_max=backoff_max,
        status_forcelist=status_forcelist,
        backoff_jitter=0.5,
        respect_retry_after_header=True,
        allowed_methods=None,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def analyze_text_sapling(text: str) -> Dict[str, Any]:
    """Analyze text using Sapling AI detector API."""
    headers = {
        "Content-Type": "application/json",
    }

    # Some articles are too long
    text = text[:10000]

    data = {"key": SAPLING_API_KEY, "text": text, "sent_scores": True}

    session = requests_retry_session(
        retries=10,
        backoff_factor=5,
        backoff_max=300,
        status_forcelist=(500, 502, 504, 429),
    )
    try:
        response = session.post(SAPLING_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    finally:
        session.close()


def analyze_text_undetectable(text: str) -> Dict[str, Any]:
    """Analyze text using Undetectable AI detector API."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    data = {
        "text": text,
        "key": UNDETECTABLE_API_KEY,
        "model": "xlm_ud_detector",
        "retry_count": 0,
    }

    session = requests_retry_session()
    try:
        # First, submit the text for analysis
        response = session.post(UNDETECTABLE_API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Wait for the analysis to complete
        time.sleep(2)  # Wait for initial processing

        # Query the result
        query_url = "https://ai-detect.undetectable.ai/query"
        query_data = {"id": result["id"]}

        for _ in range(5):  # Try up to 5 times to get the result
            query_response = session.post(query_url, headers=headers, json=query_data)
            query_result = query_response.json()

            if query_result["status"] == "done":
                return {
                    "score": query_result["result"],
                    "result_details": query_result["result_details"],
                }

            time.sleep(30)  # Wait before checking again

        raise Exception("Timeout waiting for analysis results")
    finally:
        session.close()


def analyze_text_copyleaks(text: str, post_url: str) -> Dict[str, Any]:
    """Analyze text using Copyleaks AI detector API."""
    try:
        # Extract the post ID from the URL (last component)
        scan_id = post_url.split("/")[-1]

        # Max size allowed is 25000 characters, so we need to truncate the text
        text = text[:10000]

        # Create and configure the document
        document = NaturalLanguageDocument(text)
        # document.set_sandbox(True)  # Use sandbox mode for testing

        # Submit for analysis
        response = Copyleaks.AiDetectionClient.submit_natural_language(
            copyleaks_auth_token, scan_id, document
        )

        return {
            "raw_response": response,
            "score": response.get("score", 0),
            "result_details": {
                "is_ai_generated": response.get("isAiGenerated", False),
                "confidence": response.get("confidence", 0),
                "model": response.get("model", "unknown"),
            },
        }
    except CommandError as ce:
        response = ce.get_response()
        raise Exception(f"Copyleaks API error: {response.content}")
    except Exception as e:
        raise Exception(f"Error analyzing text with Copyleaks: {str(e)}")


def analyze_text(text: str, post_url: str = "") -> Dict[str, Any]:
    """Analyze text using the configured API."""
    if DETECTOR_API == DetectorAPI.SAPLING.value:
        return analyze_text_sapling(text)
    elif DETECTOR_API == DetectorAPI.UNDETECTABLE.value:
        return analyze_text_undetectable(text)
    elif DETECTOR_API == DetectorAPI.COPYLEAKS.value:
        return analyze_text_copyleaks(text, post_url)
    else:
        raise ValueError(f"Unsupported detector API: {DETECTOR_API}")


def process_posts(
    input_file: str, output_file: str, post_type: str, limit: int | None = None
):
    """Process posts from input file and save results to output file."""
    print(f"Processing {post_type} posts...")

    # Load posts
    with open(input_file, "r") as f:
        posts = json.load(f)

    # Limit the number of posts if specified
    if limit is not None:
        posts = posts[:limit]
        print(f"Limiting to {limit} posts")

    results = []

    # Process each post
    for post in tqdm(posts):
        try:
            # Extract post content
            content = post.get("Content", "")
            if not content:
                continue

            # Get post URL for Copyleaks ID
            post_url = post.get("Link", "")

            # Analyze content
            analysis = analyze_text(content, post_url)

            # Store results
            result = {
                "link": post_url,
                "title": post.get("Title"),
                "analysis": analysis,
            }
            results.append(result)

            # Add a small delay to avoid rate limiting
            time.sleep(2)

        except Exception as e:
            print(f"Error processing post {post.get('Title')}: {str(e)}")

    # Save results
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to {output_file}")


def main():
    # Create output directory if it doesn't exist
    os.makedirs("step_3_check_APIs/results", exist_ok=True)

    # Process accepted posts
    process_posts(
        "raw_data/accepted_posts.json",
        f"step_3_check_APIs/results/accepted_posts_analysis_{DETECTOR_API}.json",
        "accepted",
        limit=10,
    )

    # Process LLM rejected posts
    process_posts(
        "step_0_data_processing/llm_rejected_posts.json",
        f"step_3_check_APIs/results/llm_rejected_posts_analysis_{DETECTOR_API}.json",
        "llm_rejected",
        limit=10,
    )

    # Process other rejected posts
    process_posts(
        "step_0_data_processing/other_rejected_posts.json",
        f"step_3_check_APIs/results/other_rejected_posts_analysis_{DETECTOR_API}.json",
        "other_rejected",
        limit=10,
    )


if __name__ == "__main__":
    main()
