import trafilatura  # For robust web page text extraction
import requests  # For fetching web pages


def scrape_urls(urls, max_length=20000):
    """
    Scrape and extract main text content from a list of URLs using trafilatura.
    Returns a dict mapping each URL to its extracted text (or None if failed).
    Limits total combined text length to max_length characters.
    """
    results = {}
    total_length = 0
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                text = trafilatura.extract(response.text, url=url)
                if text:
                    # Truncate if total length would exceed max_length
                    if total_length + len(text) > max_length:
                        text = text[:max_length - total_length]
                    results[url] = text
                    total_length += len(text)
                    if total_length >= max_length:
                        break
                else:
                    results[url] = None
            else:
                results[url] = None
        except Exception as e:
            print(f"[WebScraper] Error scraping {url}: {e}")
            results[url] = None
    return results 