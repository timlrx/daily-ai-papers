"""
summarize_papers.py

This script summarizes the daily papers pulled from Hugging Face's papers page,
updates the README with the summaries, and cleans up temporary files.
"""

# Standard library imports
import json
import os
import time
from datetime import datetime
from typing import List, Optional

# Third party imports
import google.generativeai as genai
from scripts.schemas import ClassificationChoices, PaperResponse

# Configure the Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])


categories_of_interest = [
    ClassificationChoices.MULTIMODAL,
    ClassificationChoices.TEXT_GENERATION,
    ClassificationChoices.TEXT_CLASSIFICATION,
    ClassificationChoices.TEXT2TEXT_GENERATION,
    ClassificationChoices.SUMMARIZATION,
    ClassificationChoices.QUESTION_ANSWERING,
    ClassificationChoices.NATURAL_LANGUAGE_PROCESSING,
    ClassificationChoices.AUDIO,
    ClassificationChoices.TEXT_TO_SPEECH,
    ClassificationChoices.AUDIO_TO_AUDIO,
]
categories_of_interest = [category.value for category in categories_of_interest]


def summarize_paper(
    title: str, authors: str, pdf_path: str, model_name: str, github_repo: str = ""
) -> PaperResponse:
    """
    Summarizes a research paper using the Gemini API and returns a structured response.

    Args:
    - title (str): The title of the paper.
    - authors (str): The authors of the paper.
    - pdf_path (str): The path to the PDF of the paper.
    - model_name (str): The Gemini model to use for summarization.
    - github_repo (str): The GitHub repository associated with the paper.

    Returns:
    - PaperResponse: A dictionary containing the summary, classification, and relevant URLs.
    """

    model = genai.GenerativeModel(model_name=model_name)
    github_repo = "None" if not github_repo else github_repo

    # Upload the PDF to Gemini
    pdf_file = genai.upload_file(path=pdf_path, display_name=f"paper_{title}")

    # Load the prompt template
    with open("templates/prompt_template.md", "r") as f:
        prompt_template = f.read()

    # Create the prompt with title and authors
    prompt = (
        prompt_template.replace("{title}", title)
        .replace("{authors}", authors)
        .replace("{github_repo}", github_repo)
    )

    # Get the content from the model
    response = model.generate_content(
        [pdf_file, prompt],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",  # Expect a structured JSON response
            response_schema=PaperResponse,  # Validate response to follow the PaperSummary structure
        ),
    )

    return response.text


def save_daily_results(date_str: str, papers: List[PaperResponse]) -> None:
    """
    Save the daily results as a JSON file.

    Args:
    - date_str (str): The date string in the format YYYY-MM-DD.
    - papers (List[PaperResponse]): A list of dictionaries containing paper information and summaries.
    """
    year, month, day = date_str.split("-")
    os.makedirs(f"daily_results/{year}/{month}", exist_ok=True)
    with open(f"daily_results/{year}/{month}/{day}.json", "w") as f:
        json.dump(papers, f, indent=4)


def save_consolidated_results(papers: List[PaperResponse]) -> None:
    """
    Save a consolidated running list of results as a JSON file.

    Args:
    - papers (List[PaperResponse]): A list of dictionaries containing paper information and summaries.
    """
    consolidated_path = "consolidated_results.json"
    if os.path.exists(consolidated_path):
        with open(consolidated_path, "r") as f:
            consolidated_results = json.load(f)
    else:
        consolidated_results = []

    consolidated_results.extend(papers)

    with open(consolidated_path, "w") as f:
        json.dump(consolidated_results, f, indent=4)


def archive_markdown(date_str: str, new_content: str) -> None:
    """
    Archive the markdown content for the given date.

    Args:
    - date_str (str): The date string in the format YYYY-MM-DD.
    - new_content (str): The new markdown content to be archived.
    """
    year, month, day = date_str.split("-")
    os.makedirs(f"archive/{year}/{month}", exist_ok=True)
    with open(f"archive/{year}/{month}/{day}.md", "w") as f:
        f.write(new_content)


def update_readme(date_str: str, papers: List[PaperResponse]) -> None:
    """
    Updates the README file with the summaries of the papers.

    Args:
    - date_str (str): The date string in the format YYYY-MM-DD.
    - papers (List[PaperResponse]): A list of dictionaries containing paper information and summaries.
    """
    new_content = f"\n\n## Papers for {date_str}\n\n"
    new_content += "| Title | Authors | Summary | Classification | GitHub URLs | HuggingFace URLs |\n"
    new_content += "|-------|---------|---------|----------------|-------------|-----------------|\n"

    for paper in papers:
        # Parse the summary JSON
        summary_data = json.loads(paper["summary"])

        # Replace line breaks with spaces in the summary text
        summary_text = summary_data.get("summary", "").replace("\n", " ")

        # Access classification, GitHub, and HuggingFace URLs
        classification = summary_data.get("classification", "N/A")
        github_urls = summary_data.get("github_urls", [])
        huggingface_urls = summary_data.get("huggingface_urls", [])

        # Convert GitHub and HuggingFace URLs to comma-separated strings
        github_links = (
            ", ".join([f"[Link]({url})" for url in github_urls])
            if github_urls
            else "N/A"
        )
        huggingface_links = (
            ", ".join([f"[Link]({url})" for url in huggingface_urls])
            if huggingface_urls
            else "N/A"
        )

        if any(cls in categories_of_interest for cls in classification):
            new_content += (
                f"| [{paper['title']}]({paper['link']}) "
                f"| {paper['authors']} "
                f"| {summary_text} "
                f"| {classification} "
                f"| {github_links} "
                f"| {huggingface_links} |\n"
            )

    # Archive the markdown content
    archive_markdown(date_str, new_content)

    # Flatten the results and remove pdf_path
    for paper in papers:
        summary_data = json.loads(paper["summary"])
        paper.update(summary_data)
        paper.pop("pdf_path", None)
        paper["date"] = date_str

    # Write the new content to the archive
    save_daily_results(date_str, papers)
    save_consolidated_results(papers)

    # Update the README with the new content
    # Load the existing README
    with open("README.md", "r") as f:
        existing_content = f.read()

    # Load the intro template
    with open("templates/README_intro.md", "r") as f:
        intro_content = f.read()

    # Add the date to the intro
    intro_content = intro_content.replace("{DATE}", f"{date_str} \n \n").replace(
        "{CATEGORIES_OF_INTEREST}", ", ".join(categories_of_interest)
    )

    # Remove the existing header
    front_content = existing_content.split("## Papers for")[0]
    existing_content = existing_content.replace(front_content, "")

    # Combine the intro, new content, and existing content
    updated_content = intro_content + new_content + "\n\n" + existing_content

    # Write the updated content to the README
    with open("README.md", "w") as f:
        f.write(updated_content)


def main(date: Optional[str] = None) -> None:
    """
    Main function to summarize papers, update the README, and clean up temporary files.
    """
    # Use today's date if not specified
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    with open(f"data/{date}_papers.json", "r") as f:
        papers = json.load(f)

    summaries = []
    for paper in papers:
        try:
            print(f"Summarizing paper {paper['title']}")
            summary = summarize_paper(
                title=paper["title"],
                authors=paper["authors"],
                pdf_path=paper["pdf_path"],
                model_name="gemini-1.5-pro",
                # Replace null values with empty strings
                github_repo=paper.get("github_repo", ""),
            )
            summaries.append({**paper, "summary": summary})
            time.sleep(60)  # Sleep for 1 minute to avoid rate limiting
        except Exception:
            try:
                print(
                    f"Failed to summarize paper {paper['title']}. Trying with a different model."
                )
                summary = summarize_paper(
                    title=paper["title"],
                    authors=paper["authors"],
                    pdf_path=paper["pdf_path"],
                    model_name="gemini-1.5-flash",
                    github_repo=paper.get("github_repo", ""),
                )
                summaries.append({**paper, "summary": summary})
            except Exception as e:
                print(
                    f"Failed to summarize paper {paper['title']} with both models. Due to {e}"
                )
                continue
    update_readme(date, summaries)

    # Clean up temporary PDF files
    for paper in papers:
        if os.path.exists(paper["pdf_path"]):
            os.remove(paper["pdf_path"])


if __name__ == "__main__":
    main()
