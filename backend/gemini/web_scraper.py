import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from urllib.parse import urlparse

class WebScraper:
    def __init__(self, delay: float = 1.0):
        """
        Initialize the web scraper
        Args:
            delay: Time to wait between requests (in seconds) to be polite to servers
        """
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def scrape_urls(self, urls: List[str]) -> List[Dict]:
        """
        Scrape multiple URLs and return their content
        Args:
            urls: List of URLs to scrape
        Returns:
            List of dictionaries containing scraped data
        """
        results = []
        for url in urls:
            try:
                data = self.scrape_single_url(url)
                results.append(data)
                time.sleep(self.delay)  # Be polite to servers
            except Exception as e:
                print(f"Error scraping {url}: {str(e)}")
        return results

    def scrape_single_url(self, url: str) -> Dict:
        """
        Scrape a single URL and extract relevant information
        Args:
            url: URL to scrape
        Returns:
            Dictionary containing scraped data
        """
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract basic information
        data = {
            'url': url,
            'domain': urlparse(url).netloc,
            'title': soup.title.text.strip() if soup.title else None,
            'meta_description': None,
            'headings': [],
            'links': [],
            'text_content': soup.get_text(separator=' ', strip=True),
        }

        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['meta_description'] = meta_desc.get('content', '')

        # Get all headings (h1-h6)
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            for heading in headings:
                data['headings'].append({
                    'level': i,
                    'text': heading.text.strip()
                })

        # Get all links
        for link in soup.find_all('a', href=True):
            data['links'].append({
                'text': link.text.strip(),
                'href': link['href']
            })

        return data

def main():
    # Example usage
    urls = [
        'https://example.com',
        'https://python.org'
    ]
    
    scraper = WebScraper(delay=0.01)  # 1.5 seconds delay between requests
    results = scraper.scrape_urls(urls)
    
    # Print results
    for result in results:
        print(f"\nScraped data for: {result['url']}")
        print(f"Title: {result['title']}")
        print(f"Meta Description: {result['meta_description']}")
        print(f"Number of headings: {len(result['headings'])}")
        print(f"Number of links: {len(result['links'])}")

if __name__ == "__main__":
    main()