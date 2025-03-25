import requests
from bs4 import BeautifulSoup
import urllib.parse
from typing import List, Tuple

def dynamic_news_search(query: str) -> List[Tuple[str, str]]:
    """
    Dynamically search for news headlines related to the given query
    using web scraping techniques.

    Args:
        query (str): Search query for news headlines

    Returns:
        List of tuples containing (headline, url)
    """
    # Encode the query for URL
    encoded_query = urllib.parse.quote(query)

    # List of search engines to scrape
    search_engines = [
        # Google News Search
        {
            'url': f'https://news.google.com/search?q={encoded_query}&hl=en-US&gl=US&ceid=US%3Aen',
            'selector': 'article h3 a',
            'base_url': 'https://news.google.com'
        },
        # Alternative News Search
        {
            'url': f'https://www.newsnow.co.uk/showfeed.aspx?newsuri=https://www.google.com/news/search?q={encoded_query}&output=rss',
            'selector': 'a.newslink',
            'base_url': 'https://www.newsnow.co.uk'
        }
    ]

    results = []

    for engine in search_engines:
        try:
            # Send a request with a user agent to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(engine['url'], headers=headers)

            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find headline links
            headlines = soup.select(engine['selector'])

            # Collect unique results
            for headline in headlines[:5]:  # Limit to 5 results
                title = headline.get_text().strip()
                href = headline.get('href', '').strip()

                # Ensure absolute URL
                if href.startswith('/'):
                    href = f"{engine['base_url']}{href}"

                if title and href and (title, href) not in results:
                    results.append((title, href))

                # Break if we have 5 results
                if len(results) >= 5:
                    break

        except Exception as e:
            print(f"Error scraping {engine['url']}: {e}")

    return results


def enhanced_news_search(news_headline: str):
    """
    Enhance news search by using topics and subtopics from prediction

    Args:
        news_headline (str): Input news headline

    Returns:
        List of news results with similarity scores
    """
    # Import models (assuming they're in the same directory)
    from Prediction import load_model, predict_topic_words
    from similarity import calculate_similarity

    # Load models
    tfidf_vectorizer = load_model('News Proto/tfidf_vectorizer.pkl')
    nmf_model = load_model('News Proto/nmf_model.pkl')

    # Predict topics
    primary_topic, subtopics = predict_topic_words(news_headline, tfidf_vectorizer, nmf_model)

    # Construct search query
    search_query = f"{primary_topic} {' '.join(subtopics)}"

    # Fetch dynamic news results
    search_results = dynamic_news_search(search_query)

    # Calculate similarities
    similarities = []
    harmonic_means = []

    for title, url in search_results:
        if title:
            score_dict = calculate_similarity(news_headline, title)
            similarities.append((title, url, score_dict))
            harmonic_means.append(score_dict['harmonic_mean'])

    # Calculate combined score
    combined_score = 5 / sum(1 / x for x in harmonic_means if x) if harmonic_means else 0

    return {
        'primary_topic': primary_topic,
        'subtopics': subtopics,
        'similarities': similarities,
        'combined_score': combined_score
    }


# Example usage
if __name__ == "__main__":
    test_headline = "Rohit Sharma, Virat Kohli announce retirement from T20 after world cup."
    results = enhanced_news_search(test_headline)

    print(f"Primary Topic: {results['primary_topic']}")
    print(f"Subtopics: {results['subtopics']}")
    print(f"Combined Similarity Score: {results['combined_score']}")

    print("\nSimilar News Headlines:")
    for title, url, scores in results['similarities']:
        print(f"Title: {title}")
        print(f"URL: {url}")
        print(f"Similarity Scores: {scores}\n")