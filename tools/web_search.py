from duckduckgo_search import DDGS  # For performing DuckDuckGo web searches
from tools.web_scraper import scrape_urls  # For scraping web page content
import os  # For file operations
import google.generativeai as genai  # For Gemini summarization and answer extraction
import json  # For parsing Gemini's JSON response

# Ensure search_results directory exists
RESULTS_DIR = "search_results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Use Gemini for summarization and answer extraction
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def search_duckduckgo(query, result_length="default", max_results=3):
    """
    Search DuckDuckGo for the given query, scrape the top links, summarize with Gemini, save to file,
    and extract a direct answer using Gemini. Returns (answer, file_path, results).
    'results' is a list of dicts with 'title' and 'href' only.
    """
    # 1. Search DuckDuckGo
    links = []
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            if r.get("href"):
                links.append(r["href"])
                results.append({
                    "title": r.get("title", ""),
                    "href": r.get("href", "")
                })

    # 2. Scrape content from top links
    scraped = scrape_urls(links)
    combined_text = "\n\n".join([t for t in scraped.values() if t])
    if not combined_text:
        return ("No relevant content could be scraped from the top results.", None, results)

    # 3. Summarize all content with Gemini (no intent/result_length here)
    model = genai.GenerativeModel("gemini-2.5-flash")
    summary_prompt = (
        f"Summarize the following information from multiple web pages about '{query}'. "
        "Focus on accuracy, clarity, and completeness.\n\n" + combined_text
    )
    summary_response = model.generate_content(summary_prompt)
    summary = summary_response.text.strip()

    # 4. Save full scraped text and summary to a file
    safe_query = "_".join(query.lower().split())[:50]
    file_path = os.path.join(RESULTS_DIR, f"{safe_query}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"Query: {query}\n\n---\n\n")
        f.write("Summary:\n" + summary + "\n\n---\n\n")
        for url, text in scraped.items():
            f.write(f"URL: {url}\n{text}\n\n---\n\n")

    # 5. Ask Gemini for a direct answer to the original question, using the summary and result_length
    if result_length == "short":
        answer_prompt = (
            f"Based on the following summary, answer the question as directly as possible in 1-2 informative sentences.\n"
            f"Question: {query}\n\nSummary:\n{summary}"
        )
    elif result_length == "detailed":
        answer_prompt = (
            f"Based on the following summary, answer the question in a well-structured paragraph or two, providing as much relevant detail as possible.\n"
            f"Question: {query}\n\nSummary:\n{summary}"
        )
    else:
        answer_prompt = (
            f"Based on the following summary, answer the question concisely but completely.\n"
            f"Question: {query}\n\nSummary:\n{summary}"
        )
    answer_response = model.generate_content(answer_prompt)
    answer = answer_response.text.strip()

    # 6. Return the answer, file path, and results (links only)
    return (answer, file_path, results) 