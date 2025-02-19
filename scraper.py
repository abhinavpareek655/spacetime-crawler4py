import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def scraper(url, resp):
    if resp.status != 200 or not resp.raw_response:
        return []
    
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    """
    Extracts valid hyperlinks from the page content.
    """
    links = []
    try:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            absolute_link = urljoin(url, a_tag["href"])  # Convert relative URLs to absolute
            links.append(absolute_link)
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
    
    return links

def is_valid(url):
    """
    Determines whether a URL should be crawled.
    """
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in {"http", "https"}:
            return False
        
        # Allow only specific UCI domains
        allowed_domains = {"ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu"}
        if parsed.netloc not in allowed_domains:
            return False
        
        # Remove fragment part from URLs
        if "#" in parsed.path:
            return False
        
        # Filter out non-text file types
        if re.match(r".*\.(css|js|bmp|gif|jpe?g|ico|png|tiff?|mp2|mp3|mp4|wav|avi|mov|mpeg|pdf|docx?|pptx?|xlsx?)$", parsed.path.lower()):
            return False
        
        return True
    
    except Exception as e:
        print(f"Error validating URL {url}: {e}")
        return False
