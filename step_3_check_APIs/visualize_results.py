import streamlit as st
import json
import pandas as pd
from pathlib import Path
import numpy as np

# Set page config
st.set_page_config(
    page_title="LessWrong Post Analysis Results", page_icon="📊", layout="wide"
)

# Title
st.title("LessWrong Post Analysis Results")

# Create tabs for different services
sapling_tab, copyleaks_tab = st.tabs(["Sapling Results", "Copyleaks Results"])


# Function to load and process Sapling data
@st.cache_data
def load_sapling_data():
    # Load the JSON files
    results_dir = Path("results")
    if not results_dir.exists():
        results_dir = Path("step_3_check_APIs/results")
        if not results_dir.exists():
            raise FileNotFoundError(
                f"Results directory not found at {results_dir} or step_3_check_APIs/results"
            )

    with open(results_dir / "accepted_posts_analysis_sapling.json", "r") as f:
        accepted_data = json.load(f)

    with open(results_dir / "llm_rejected_posts_analysis_sapling.json", "r") as f:
        llm_rejected_data = json.load(f)

    with open(results_dir / "other_rejected_posts_analysis_sapling.json", "r") as f:
        other_rejected_data = json.load(f)

    # Create DataFrames
    accepted_df = pd.DataFrame(
        [
            {
                "title": item["title"],
                "link": item["link"],
                "score": item["analysis"]["score"],
                "type": "Accepted",
                "full_data": item,
            }
            for item in accepted_data
        ]
    )

    llm_rejected_df = pd.DataFrame(
        [
            {
                "title": item["title"],
                "link": item["link"],
                "score": item["analysis"]["score"],
                "type": "LLM Rejected",
                "full_data": item,
            }
            for item in llm_rejected_data
        ]
    )

    other_rejected_df = pd.DataFrame(
        [
            {
                "title": item["title"],
                "link": item["link"],
                "score": item["analysis"]["score"],
                "type": "Other Rejected",
                "full_data": item,
            }
            for item in other_rejected_data
        ]
    )

    return accepted_df, llm_rejected_df, other_rejected_df


# Function to load and process Copyleaks data
@st.cache_data
def load_copyleaks_data():
    results_dir = Path("results")
    if not results_dir.exists():
        results_dir = Path("step_3_check_APIs/results")
        if not results_dir.exists():
            raise FileNotFoundError(
                f"Results directory not found at {results_dir} or step_3_check_APIs/results"
            )

    with open(results_dir / "accepted_posts_analysis_copyleaks.json", "r") as f:
        accepted_data = json.load(f)

    with open(results_dir / "llm_rejected_posts_analysis_copyleaks.json", "r") as f:
        llm_rejected_data = json.load(f)

    with open(results_dir / "other_rejected_posts_analysis_copyleaks.json", "r") as f:
        other_rejected_data = json.load(f)

    # Create DataFrames
    accepted_df = pd.DataFrame(
        [
            {
                "title": item["title"],
                "link": item["link"],
                "probability": item["analysis"]["raw_response"]["results"][0][
                    "probability"
                ],
                "classification": item["analysis"]["raw_response"]["results"][0][
                    "classification"
                ],
                "classification_text": (
                    "Human"
                    if item["analysis"]["raw_response"]["results"][0]["classification"]
                    == 1
                    else "AI"
                ),
                "type": "Accepted",
                "full_data": item,
            }
            for item in accepted_data
        ]
    )

    llm_rejected_df = pd.DataFrame(
        [
            {
                "title": item["title"],
                "link": item["link"],
                "probability": item["analysis"]["raw_response"]["results"][0][
                    "probability"
                ],
                "classification": item["analysis"]["raw_response"]["results"][0][
                    "classification"
                ],
                "classification_text": (
                    "Human"
                    if item["analysis"]["raw_response"]["results"][0]["classification"]
                    == 1
                    else "AI"
                ),
                "type": "LLM Rejected",
                "full_data": item,
            }
            for item in llm_rejected_data
        ]
    )

    other_rejected_df = pd.DataFrame(
        [
            {
                "title": item["title"],
                "link": item["link"],
                "probability": item["analysis"]["raw_response"]["results"][0][
                    "probability"
                ],
                "classification": item["analysis"]["raw_response"]["results"][0][
                    "classification"
                ],
                "classification_text": (
                    "Human"
                    if item["analysis"]["raw_response"]["results"][0]["classification"]
                    == 1
                    else "AI"
                ),
                "type": "Other Rejected",
                "full_data": item,
            }
            for item in other_rejected_data
        ]
    )

    return accepted_df, llm_rejected_df, other_rejected_df


# Function to display a table for a given DataFrame
def display_sapling_table(df, title):
    st.header(title)
    st.info("Select a row to view the full post data on the right side")

    # Create two columns
    col1, col2 = st.columns([2, 1])

    selected_post = None

    with col1:
        # Create a styled DataFrame
        def color_score(val):
            # Only apply color to numeric values (the score column)
            if not isinstance(val, (int, float)):
                return ""

            if val >= 0.9:
                return "background-color: rgba(255, 0, 0, 0.2)"  # Light red
            elif val <= 0.1:
                return "background-color: rgba(0, 255, 0, 0.2)"  # Light green
            else:
                # Gradient from green to red
                intensity = (val - 0.1) / 0.8  # Normalize to 0-1
                return f"background-color: rgba({int(255 * intensity)}, {int(255 * (1 - intensity))}, 0, 0.2)"

        # Apply styling to the DataFrame
        styled_df = df[["title", "link", "score"]].style.apply(
            lambda x: [color_score(v) for v in x], axis=0
        )

        # Display the styled table with clickable links
        state = st.dataframe(
            styled_df,
            column_config={
                "title": "Title",
                "link": st.column_config.LinkColumn(
                    "Link",
                    display_text="LessWrong",
                    help="Click to view post on LessWrong",
                ),
                "score": st.column_config.NumberColumn(
                    "AI Detection Score",
                    format="%.6f",
                ),
            },
            hide_index=True,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun",
        )

        if state and len(state.selection.rows) > 0:
            selected_post = state.selection.rows[0]

    with col2:
        if selected_post is not None:
            st.subheader("Selected Post Details")
            st.json(df.iloc[selected_post]["full_data"])


def display_copyleaks_table(df, title):
    st.header(title)
    st.info("Select a row to view the full post data on the right side")

    # Create two columns
    col1, col2 = st.columns([2, 1])

    selected_post = None

    with col1:
        # Create a styled DataFrame
        def color_score(val, col):
            # Only apply color to numeric values
            if not isinstance(val, (int, float)):
                return ""

            if col == "probability":
                if val >= 0.9:
                    return "background-color: rgba(255, 0, 0, 0.2)"  # Light red
                elif val <= 0.1:
                    return "background-color: rgba(0, 255, 0, 0.2)"  # Light green
                else:
                    # Gradient from green to red
                    intensity = (val - 0.1) / 0.8  # Normalize to 0-1
                    return f"background-color: rgba({int(255 * intensity)}, {int(255 * (1 - intensity))}, 0, 0.2)"
            elif col == "classification_text":
                if val == "AI":
                    return "background-color: rgba(255, 0, 0, 0.2)"
                elif val == "Human":
                    return "background-color: rgba(0, 255, 0, 0.2)"

        # Apply styling to the DataFrame
        styled_df = df[
            ["title", "link", "probability", "classification_text"]
        ].style.apply(lambda x: [color_score(v, x.name) for v in x], axis=0)

        # Display the styled table with clickable links
        state = st.dataframe(
            styled_df,
            column_config={
                "title": "Title",
                "link": st.column_config.LinkColumn(
                    "Link",
                    display_text="LessWrong",
                    help="Click to view post on LessWrong",
                ),
                "probability": st.column_config.NumberColumn(
                    "AI Probability",
                    format="%.6f",
                ),
                "classification_text": st.column_config.TextColumn(
                    "Classification",
                ),
            },
            hide_index=True,
            use_container_width=True,
            selection_mode="single-row",
            on_select="rerun",
        )

        if state and len(state.selection.rows) > 0:
            selected_post = state.selection.rows[0]

    with col2:
        if selected_post is not None:
            st.subheader("Selected Post Details")
            st.json(df.iloc[selected_post]["full_data"])


# Load the data
sapling_accepted_df, sapling_llm_rejected_df, sapling_other_rejected_df = (
    load_sapling_data()
)
copyleaks_accepted_df, copyleaks_llm_rejected_df, copyleaks_other_rejected_df = (
    load_copyleaks_data()
)

# Display Sapling results
with sapling_tab:
    display_sapling_table(sapling_accepted_df, "Accepted Posts")
    display_sapling_table(sapling_llm_rejected_df, "LLM Rejected Posts")
    display_sapling_table(sapling_other_rejected_df, "Other Rejected Posts")

# Display Copyleaks results
with copyleaks_tab:
    display_copyleaks_table(copyleaks_accepted_df, "Accepted Posts")
    display_copyleaks_table(copyleaks_llm_rejected_df, "LLM Rejected Posts")
    display_copyleaks_table(copyleaks_other_rejected_df, "Other Rejected Posts")
