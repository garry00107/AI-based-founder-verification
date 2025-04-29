# scraper.py
import time
import random
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from analyzer import analyze_sentiment # Used for web sentiment search
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Constants and Configuration ---
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
]

# --- Helper Functions ---
def get_random_user_agent():
    return random.choice(USER_AGENTS)

# --- Selenium Setup (Keep as before) ---
def setup_selenium_driver():
    """Sets up Selenium WebDriver (Keep as before, simplified logging)"""
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={get_random_user_agent()}')
    # chrome_options.add_argument("--headless") # Uncomment for server deployment
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver
    except Exception as e:
        logging.error(f"Error setting up Selenium driver: {e}")
        return None

def random_delay(min_seconds=1, max_seconds=3):
    time.sleep(random.uniform(min_seconds, max_seconds))

# --- LinkedIn Scraping (Keep Simulated Version) ---
def scrape_linkedin_profile(profile_url, linkedin_email, linkedin_password):
    """Simulated LinkedIn Scraper."""
    logging.info(f"Simulating LinkedIn data fetch for: {profile_url}")
    query_name = profile_url.split('/')[-1].replace('-', ' ').title() # Crude name extraction
    return {
        "profile_url": "#", "name": f"{query_name} (Simulated)",
        "headline": "Founder | Visionary (Simulated)", "location": "San Francisco Bay Area (Simulated)",
        "experience": [{"title": "CEO", "company": f"{query_name} Inc (Simulated)", "duration": "2020-Present", "description":"Building the next big thing (Simulated)."}],
        "education": [{"institution": "University of Innovation (Simulated)", "degree": "M.Sc.", "years": "2015-2019"}],
        "error": "Using simulated LinkedIn data for demonstration."
    }

# --- Industry Identification and Learnings (Keep as before, maybe expand DB) ---
INDUSTRY_KEYWORDS = {
    "Quick Commerce": ["zepto", "blinkit", "swiggy instamart", "getir", "gorillas", "fast delivery", "10 minute delivery"],
    "FinTech": ["fintech", "payment", "lending", "insurtech", "crypto", "blockchain", "wealthtech", "paytm", "razorpay", "stripe"],
    "SaaS": ["saas", "software", "cloud", "crm", "erp", "subscription software", "freshworks", "zoho", "salesforce"],
    "EdTech": ["edtech", "education", "online learning", "tutoring", "skill development", "byjus", "unacademy", "coursera"],
    "HealthTech": ["healthtech", "telemedicine", "digital health", "medical", "pharma", "practo", "apollo 247"],
    "E-commerce": ["ecommerce", "marketplace", "online retail", "shopping", "dtc", "d2c", "flipkart", "amazon", "meesho"],
    "Logistics": ["logistics", "supply chain", "shipping", "transportation", "fulfillment", "delhivery", "rivigo"],
    "AI/ML": ["artificial intelligence", "machine learning", "ai ", " ml ", "deep learning"],
    "Social Media": ["social media", "networking", "community", "facebook", "instagram", "twitter", "linkedin"],
    "Gaming": ["gaming", "esports", "mobile game", "console", "pc game"],
    "FoodTech": ["food delivery", "restaurant tech", "cloud kitchen", "zomato", "swiggy"]
}

INDUSTRY_LEARNINGS_DB = {
    "Quick Commerce": {
        "title": "Quick Commerce Industry Insights",
        "content": [
            "Challenges: Intense competition, high cash burn, complex unit economics (delivery costs vs basket size), rider safety & gig worker regulations, inventory spoilage.",
            "Trends: Focus on profitability over hyper-growth, consolidation, diversifying into adjacent services (ads, private labels), optimizing delivery routes and dark store density.",
            "Key Factors: Dark store location strategy, supply chain efficiency, inventory management (predictive ordering), delivery speed & reliability, customer retention (loyalty programs).",
        ]
    },
    "FinTech": {
        "title": "FinTech Industry Insights",
        "content": [
            "Challenges: Navigating complex regulations (differs by region), cybersecurity threats & fraud prevention, building customer trust, intense competition from incumbents & neo-banks, achieving profitability at scale.",
            "Trends: Embedded finance (integrating financial services into non-financial platforms), open banking APIs, Buy Now Pay Later (BNPL), AI/ML for risk assessment & personalization, CBDCs (Central Bank Digital Currencies), increasing regulatory scrutiny.",
            "Key Factors: Robust compliance framework, seamless user experience (UX), data security & privacy, strategic partnerships, scalable & reliable infrastructure.",
        ]
    },
     "SaaS": {
        "title": "SaaS Industry Insights",
        "content": [
            "Challenges: High customer acquisition costs (CAC), minimizing churn (customer retention), demonstrating clear value & ROI, integration complexity with existing systems, market saturation in established categories.",
            "Trends: Rise of Vertical SaaS (industry-specific solutions), AI integration for automation & insights, usage-based pricing models, focus on Net Revenue Retention (NRR), Product-Led Growth (PLG) strategies.",
            "Key Factors: Solving a specific, significant pain point, achieving strong product-market fit, effective multi-channel sales & marketing, dedicated customer success management, scalable and secure cloud infrastructure.",
        ]
    },
    "EdTech": {
        "title": "EdTech Industry Insights",
        "content": [
            "Challenges: Ensuring pedagogical effectiveness & student engagement, high cost of content creation, scaling personalized learning, digital divide & accessibility issues, proving learning outcomes, teacher/institution adoption.",
            "Trends: Hybrid learning models, micro-learning & skill-based platforms, AI-powered adaptive learning paths, immersive technologies (AR/VR), focus on lifelong learning & workforce development.",
            "Key Factors: Quality of content & instruction design, engaging user experience, demonstrating measurable learning gains, affordability & accessibility, strong distribution channels.",
        ]
    },
    # Add more industries here...
    "Default": {
         "title": "General Startup & Tech Industry Insights",
         "content": [
             "Common Challenges: Achieving product-market fit, securing adequate funding & managing cash flow, building & retaining a talented team, scaling operations efficiently, intense competition & rapid market changes.",
             "Key Success Factors: Deep understanding of the target customer and market need, agility & adaptability, clear value proposition & differentiation, effective execution & operational excellence, resilient & visionary leadership.",
             "Current Trends: Increased focus on sustainable growth and profitability ('default alive'), importance of data analytics & AI across functions, remote/hybrid work models, cybersecurity as a critical priority.",
        ]
    }
}

def _identify_industry(query):
    """Basic keyword matching to guess industry."""
    query_lower = query.lower()
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        if any(keyword in query_lower for keyword in keywords):
            logging.info(f"Identified potential industry: {industry} for query: '{query}'")
            return industry
    logging.info(f"Could not identify specific industry for query: '{query}'")
    return None

def _get_industry_learnings(industry):
    """Fetch hardcoded learnings based on industry."""
    lookup_key = industry if industry and industry in INDUSTRY_LEARNINGS_DB else "Default"
    logging.info(f"Fetching learnings for industry key: {lookup_key}")
    return INDUSTRY_LEARNINGS_DB[lookup_key]

# --- Renamed Function: Checks Failory AND provides Industry Insights ---
def get_failure_and_industry_insights(founder_or_startup_name):
    """
    Attempts to scrape Failory for specific failure stories.
    Independently identifies the likely industry and provides generic learnings for it.
    """
    logging.info(f"Getting Failure/Industry Insights for: {founder_or_startup_name}")
    insights_data = {
        "source": "Failory Scrape & Internal KB",
        "failory_search_url": None,
        "specific_failure_found": False, # Specifically from Failory scrape
        "failure_details": [], # Stores scraped details if found via Failory
        "failed_startups": [], # Simple list of names if specific failure found (for score penalty)
        "identified_industry": None, # Store the identified industry
        "industry_learnings": None, # Stores fallback/general industry info
        "error": None # Store errors encountered during Failory scrape specifically
    }

    # 1. Identify Industry (always do this)
    industry = _identify_industry(founder_or_startup_name)
    insights_data["identified_industry"] = industry
    insights_data["industry_learnings"] = _get_industry_learnings(industry) # Get learnings regardless

    # 2. Attempt to Scrape Failory for specific failure details
    search_query = '+'.join(founder_or_startup_name.split())
    search_url = f"https://www.failory.com/search?query={search_query}"
    insights_data["failory_search_url"] = search_url
    headers = {'User-Agent': get_random_user_agent()}

    try:
        logging.info(f"Attempting Failory scrape at: {search_url}")
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Look for results (selectors might need updating)
        results_container = soup.find('div', class_='fs-cmsfilter_list') or soup
        possible_links = results_container.find_all('a', href=True)
        relevant_link_found = False
        failure_keywords = ['/cemetery', '/graveyard', '/failed-startups', '/post-mortem', '/interview']

        for link in possible_links:
            href = link.get('href', '')
            link_text_lower = link.text.lower()
            # Basic query matching (can be improved)
            query_parts = [part for part in founder_or_startup_name.lower().split() if len(part) > 2]
            is_failure_link = any(keyword in href for keyword in failure_keywords)
            matches_query = any(part in link_text_lower for part in query_parts) or any(part in href for part in query_parts)

            if is_failure_link and matches_query:
                if not href.startswith('http'): href = f"https://www.failory.com{href}"
                logging.info(f"Found potential Failory failure link: {href}")
                try:
                    # Scrape the specific failure page
                    page_response = requests.get(href, headers=headers, timeout=15)
                    page_response.raise_for_status()
                    page_soup = BeautifulSoup(page_response.text, 'lxml')

                    title_elem = page_soup.find('h1')
                    title_text = title_elem.text.strip() if title_elem else "Failory Article"

                    content_div = page_soup.find('div', class_='rich-text-block') or page_soup.find('article')
                    paragraphs = content_div.find_all(['p', 'li']) if content_div else []
                    snippet = "\n".join([p.text.strip() for p in paragraphs if p.text.strip()]) # Join non-empty paragraphs

                    # Basic reason/advice extraction (can be improved)
                    reasons = [p.text.strip() for p in paragraphs if "reason for failure" in p.text.lower() or "why we failed" in p.text.lower()][:3]
                    advice = [p.text.strip() for p in paragraphs if "advice for founders" in p.text.lower() or "lessons learned" in p.text.lower()][:3]

                    failure_summary = {
                        "title": title_text,
                        "url": href,
                        "snippet": snippet, # Store full snippet from page
                        "potential_reasons": reasons,
                        "potential_advice": advice
                    }
                    insights_data["failure_details"].append(failure_summary)
                    # Only populate 'failed_startups' if we successfully scrape details
                    insights_data["failed_startups"].append({"name": founder_or_startup_name, "source_url": href})
                    insights_data["specific_failure_found"] = True
                    relevant_link_found = True
                    logging.info(f"Successfully scraped failure details from: {href}")
                    # break # Optional: Stop after first relevant link

                except requests.exceptions.RequestException as page_e:
                    logging.warning(f"Could not fetch Failory page {href}: {page_e}")
                    if not insights_data["error"]: insights_data["error"] = f"Error fetching Failory page: {page_e}"
                except Exception as page_e:
                    logging.warning(f"Error parsing Failory page {href}: {page_e}")
                    if not insights_data["error"]: insights_data["error"] = f"Error parsing Failory page: {page_e}"

        if not relevant_link_found:
            logging.info(f"No specific failure links found on Failory for '{founder_or_startup_name}'.")
            # No error message needed here, as industry insights are provided anyway

    except requests.exceptions.RequestException as e:
        insights_data["error"] = f"Could not reach Failory search: {e}"
        logging.error(f"Failory scraping error: {e}")
    except Exception as e:
        insights_data["error"] = f"An unexpected error during Failory processing: {e}"
        logging.error(f"Failory processing error: {e}")

    # Clean up failed_startups if no specific details were actually added
    if not insights_data["failure_details"]:
        insights_data["failed_startups"] = []
        insights_data["specific_failure_found"] = False


    logging.info("Failure/Industry Insights retrieval finished.")
    return insights_data

# --- General Web Scraping for Sentiment (Keep as before) ---
def search_web_for_sentiment(query):
    """Performs a general web search (using DuckDuckGo) for overall sentiment."""
    logging.info(f"Searching web for general sentiment about: {query}")
    search_engine_url = "https://html.duckduckgo.com/html/"
    params = {'q': query}
    headers = {'User-Agent': get_random_user_agent()}
    results = {"snippets": [], "overall_sentiment": {}, "error": None}
    all_text = ""

    try:
        response = requests.post(search_engine_url, data=params, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        result_divs = soup.find_all('div', class_='result__body')

        if not result_divs:
             logging.warning("Could not find primary result divs on DDG, trying alternatives...")
             result_divs = soup.find_all('td', class_='result-link') # Example fallback

        snippet_count = 0
        for div in result_divs:
            if snippet_count >= 10: break # Limit results
            snippet_tag = div.find('a', class_='result__snippet')
            if snippet_tag:
                snippet = snippet_tag.text.strip()
                if snippet: # Avoid empty snippets
                    results["snippets"].append(snippet)
                    all_text += snippet + " . "
                    snippet_count += 1

        if not results["snippets"]:
             logging.warning("Could not extract any snippets from DuckDuckGo results page.")
             results["error"] = "Failed to parse search result snippets."
             all_text = f"Search for {query} yielded no text snippets for sentiment analysis." # Default text

        results["overall_sentiment"] = analyze_sentiment(all_text)

    except requests.exceptions.RequestException as e:
        results["error"] = f"Web search request failed: {e}"
        logging.error(f"Web search error: {e}")
        results["overall_sentiment"] = analyze_sentiment("") # Neutral sentiment on error
    except Exception as e:
        results["error"] = f"An unexpected error occurred during web search: {e}"
        logging.error(f"Web search error: {e}")
        results["overall_sentiment"] = analyze_sentiment("")

    logging.info(f"Web sentiment search finished. Overall sentiment: {results['overall_sentiment']}")
    return results

# --- Controversies Search (Keep as before) ---
def search_for_controversies(query):
    """Performs a targeted web search for potential controversies, lawsuits, scandals, etc."""
    logging.info(f"Searching web for potential controversies about: {query}")
    controversy_query = f'"{query}" controversy OR lawsuit OR scandal OR allegations OR dispute OR fraud OR investigation'
    search_engine_url = "https://html.duckduckgo.com/html/"
    params = {'q': controversy_query}
    headers = {'User-Agent': get_random_user_agent()}
    results = {
        "source": "Web Search (Controversies)",
        "search_query": controversy_query,
        "potential_hits": [],
        "error": None
    }
    controversy_keywords = [
        "controversy", "lawsuit", "sued", "scandal", "allegations", "alleged",
        "dispute", "fraud", "investigation", "settlement", "complaint",
        "misconduct", "unethical", "violation", "warning", "fine", "penalty"
    ]

    try:
        response = requests.post(search_engine_url, data=params, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        result_divs = soup.find_all('div', class_='result__body')

        if not result_divs:
             logging.warning("Could not find primary result divs on DDG for controversy search.")

        hit_count = 0
        for div in result_divs:
            if hit_count >= 7: break # Limit hits
            snippet_tag = div.find('a', class_='result__snippet')
            title_tag = div.find('a', class_='result__a')
            link_url = title_tag['href'] if title_tag and title_tag.has_attr('href') else '#' # Safer access

            if snippet_tag:
                snippet_text = snippet_tag.text.strip()
                title_text = title_tag.text.strip() if title_tag else "Result Title"
                # Check if snippet text OR title contains any controversy keywords
                text_to_check = (snippet_text + " " + title_text).lower()
                if any(keyword in text_to_check for keyword in controversy_keywords):
                     hit = {
                         "snippet": snippet_text, # Store full snippet
                         "title": title_text,
                         "url": link_url
                     }
                     results["potential_hits"].append(hit)
                     hit_count += 1
                     logging.info(f"Found potential controversy snippet: {title_text} - {snippet_text[:80]}...")

        if not results["potential_hits"]:
             logging.info("No snippets matching controversy keywords found.")
             results["error"] = "No specific controversy-related snippets found in preliminary web search."

    except requests.exceptions.RequestException as e:
        results["error"] = f"Controversy search request failed: {e}"
        logging.error(f"Controversy search error: {e}")
    except Exception as e:
        results["error"] = f"An unexpected error occurred during controversy search: {e}"
        logging.error(f"Controversy search error: {e}")

    logging.info(f"Controversy search finished. Found {len(results['potential_hits'])} potential hits.")
    return results