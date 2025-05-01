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


# Function to load and process data
@st.cache_data
def load_data():
    # Load the JSON files
    results_dir = Path("results")

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


# Load the data
accepted_df, llm_rejected_df, other_rejected_df = load_data()


# Function to display a table for a given DataFrame
def display_table(df, title):
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
            print(repr(selected_post))

    with col2:
        if selected_post is not None:
            st.subheader("Selected Post Details")
            st.json(df.iloc[selected_post]["full_data"])


# Display tables for each category
display_table(accepted_df, "Accepted Posts")
display_table(llm_rejected_df, "LLM Rejected Posts")
display_table(other_rejected_df, "Other Rejected Posts")
