import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import json

def _get_soup(url: str, timeout: int = 10):
    """
    Helper to fetch a URL and return a BeautifulSoup object.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def _create_error_response(url: str, error_msg: str, mode: str) -> dict:
    """Standardized error dictionary."""
    base = {
        'success': False,
        'url': url,
        'title': "Error",
        'error': error_msg
    }
    if mode == 'summary':
        base.update({'summary': "", 'word_count': 0})
    else:
        base.update({'links': []})
    return base

def scrape_and_summarize_website(url: str, max_summary_length: int = 500) -> dict:
    """
    Scrapes a basic HTML website and provides a summary of its text content.

    Args:
        url (str): The URL of the website to scrape.
        max_summary_length (int): The maximum number of characters for the summary.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): True if scraping was successful, False otherwise.
            - 'url' (str): The URL that was scraped.
            - 'title' (str): The title of the webpage.
            - 'summary' (str): A summary of the page's text content.
            - 'word_count' (int): The total number of words extracted.
            - 'error' (str, optional): An error message if an issue occurred.
    """
    try:
        soup = _get_soup(url)

        # Extract title
        title = soup.title.string if soup.title else "No Title Found"

        # Remove script and style elements to clean text content
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()

        # Get text and clean up whitespace
        text_content = soup.get_text(separator=' ', strip=True)

        # Summarize
        words = text_content.split()
        word_count = len(words)

        summary = text_content[:max_summary_length]
        if len(text_content) > max_summary_length:
            summary += "..." # Indicate truncation

        return {
            'success': True,
            'url': url,
            'title': title,
            'summary': summary,
            'word_count': word_count
        }

    except requests.exceptions.RequestException as e:
        return _create_error_response(url, f"Network error: {e}", 'summary')
    except Exception as e:
        return _create_error_response(url, f"Unexpected error: {e}", 'summary')

def extract_links_from_website(url: str) -> dict:
    """
    Scrapes a basic HTML website and extracts all unique absolute links.
    Args:
        url (str): The URL of the website to scrape.

    Returns:
        dict: A dictionary containing:
            - 'success' (bool): True if scraping was successful, False otherwise.
            - 'url' (str): The URL that was scraped.
            - 'links' (list): A list of unique absolute URLs found on the page.
            - 'error' (str, optional): An error message if an issue occurred.
    """
    unique_links = set()
    try:
        soup = _get_soup(url)

        # Find all <a> tags and extract href attributes
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            absolute_url = urljoin(url, href)

            # Basic validation to ensure it's a valid HTTP/HTTPS URL
            parsed_url = urlparse(absolute_url)
            if parsed_url.scheme in ['http', 'https']:
                unique_links.add(absolute_url)

        return {
            'success': True,
            'url': url,
            'links': sorted(list(unique_links)) # Return sorted list for consistent output
        }

    except requests.exceptions.RequestException as e:
        return _create_error_response(url, f"Network error: {e}", 'links')
    except Exception as e:
        return _create_error_response(url, f"Unexpected error: {e}", 'links')

def dump_as_json(data):
    return json.dumps(data, indent= 4)