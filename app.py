# app.py
from flask import Flask, render_template, request, jsonify, url_for
import scraper
import analyzer
from cache import init_cache, cache
import os
import logging
import csv # Import csv module
from datetime import datetime # Import datetime for timestamp
import threading # Import threading for lock

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask App
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-in-prod-to-a-real-secret-key!")

# Initialize caching
init_cache(app)

# --- Configuration ---
LINKEDIN_EMAIL = os.environ.get("LINKEDIN_EMAIL", "your_linkedin_email@example.com")
LINKEDIN_PASSWORD = os.environ.get("LINKEDIN_PASSWORD", "your_linkedin_password")

# --- CSV Logging Setup ---
CSV_FILE = 'search_log.csv'
# Define explicit fieldnames for the CSV header
CSV_FIELDNAMES = [
    'timestamp', 'query', 'reputation_score', 'sentiment_label',
    'linkedin_name', 'linkedin_location', 'linkedin_error',
    'industry_identified', 'failory_specific_failure_found', 'failory_error',
    'controversy_hits_count', 'controversies_error',
    'location_names_found', 'cache_status'
]
# Create a lock for thread-safe file writing (important if using multi-process/thread server)
csv_lock = threading.Lock()

def log_search_to_csv(data, cache_status):
    """Appends search data to the CSV log file."""
    log_entry = {}
    try:
        # Prepare data for logging - handle potential missing keys gracefully
        log_entry['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry['query'] = data.get('query', 'N/A')
        log_entry['reputation_score'] = data.get('analysis', {}).get('reputation_score', 'N/A')
        log_entry['sentiment_label'] = data.get('analysis', {}).get('sentiment_label', 'N/A')

        # LinkedIn Data
        linkedin_data = data.get('linkedin', {})
        log_entry['linkedin_name'] = linkedin_data.get('name', 'N/A')
        log_entry['linkedin_location'] = linkedin_data.get('location', 'N/A')
        log_entry['linkedin_error'] = linkedin_data.get('error', '')

        # Industry/Failory Data
        insights_data = data.get('failure_industry_insights', {}) # Use the new key name here
        log_entry['industry_identified'] = insights_data.get('identified_industry', 'N/A')
        log_entry['failory_specific_failure_found'] = insights_data.get('specific_failure_found', False)
        log_entry['failory_error'] = insights_data.get('error', '')

        # Controversies Data
        controversies_data = data.get('controversies', {})
        log_entry['controversy_hits_count'] = len(controversies_data.get('potential_hits', []))
        log_entry['controversies_error'] = controversies_data.get('error', '')

        # Location Data
        locations = data.get('analysis', {}).get('locations', [])
        log_entry['location_names_found'] = ", ".join([loc.get('name', '') for loc in locations if loc.get('name')]) if locations else ''

        log_entry['cache_status'] = cache_status

        # Use lock to ensure thread safety when writing
        with csv_lock:
            # Check if file exists to write header
            file_exists = os.path.isfile(CSV_FILE)
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDNAMES)
                if not file_exists or os.path.getsize(CSV_FILE) == 0:
                    writer.writeheader() # Write header only if file is new or empty
                writer.writerow(log_entry)
            logging.info(f"Successfully logged search for '{log_entry['query']}' to {CSV_FILE}")

    except Exception as e:
        logging.error(f"Error writing to CSV log for query '{data.get('query', 'N/A')}': {e}")
        # Log the problematic entry data for debugging if possible
        logging.error(f"Data that caused error: {log_entry}")


# --- Routes ---

@app.route('/')
def index():
    """Renders the home page with the search form."""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """Handles the search query, triggers scraping/analysis, and returns results."""
    query = request.form.get('query')
    if not query:
        return render_template('index.html', error="Please enter a founder or startup name.")

    normalized_query = query.lower().strip()
    cache_key = f"founder_data_{normalized_query.replace(' ', '_').replace('/', '_')}"
    logging.info(f"Received search query: '{query}' (Normalized: '{normalized_query}', Cache Key: '{cache_key}')")

    founder_data = None
    cache_status = "HIT" # Assume hit initially

    # --- Manual Caching Logic ---
    cached_data = cache.get(cache_key)
    if cached_data:
        logging.info(f"Cache HIT for query: '{query}' (Key: '{cache_key}')")
        founder_data = cached_data
        # Note: We don't log cache hits to CSV by default, but could add it here if needed.
        return render_template('results.html', data=founder_data)
    else:
        logging.info(f"Cache MISS for query: '{query}' (Key: '{cache_key}'). Fetching data...")
        cache_status = "MISS" # Update cache status
        # --- Data Fetching and Analysis (if not in cache) ---
        try:
            # 1. LinkedIn (Simulated)
            logging.info("Fetching (simulated) LinkedIn data...")
            linkedin_profile_url_placeholder = f"https://www.linkedin.com/in/{normalized_query.replace(' ','-')}"
            linked_data = scraper.scrape_linkedin_profile(linkedin_profile_url_placeholder, LINKEDIN_EMAIL, LINKEDIN_PASSWORD)

            # 2. Failure/Industry Insights (Refactored Scraper)
            logging.info("Fetching Failure/Industry insights...")
            failure_industry_insights = scraper.get_failure_and_industry_insights(query) # Use new function

            # 3. General Web Sentiment
            logging.info("Fetching web sentiment data...")
            web_sentiment_data_raw = scraper.search_web_for_sentiment(query)

            # 4. Controversies Search
            logging.info("Fetching controversies data...")
            controversies_data = scraper.search_for_controversies(query)

            # --- Process Web Snippets for Sentiment (Backend Analysis) ---
            analyzed_web_snippets = []
            if web_sentiment_data_raw and web_sentiment_data_raw.get("snippets"):
                logging.info(f"Analyzing {len(web_sentiment_data_raw['snippets'])} web snippets individually...")
                for snippet_text in web_sentiment_data_raw.get("snippets", []):
                    if isinstance(snippet_text, str) and snippet_text.strip():
                        snippet_sentiment = analyzer.analyze_sentiment(snippet_text)
                        analyzed_web_snippets.append({"text": snippet_text, "sentiment": snippet_sentiment})
                    else: logging.warning(f"Skipping invalid snippet for analysis: {snippet_text}")
            else: logging.info("No web snippets found to analyze individually.")

            # --- Data Aggregation and Structuring ---
            logging.info("Aggregating fetched data...")
            founder_data = {
                "query": query,
                "linkedin": linked_data,
                "failure_industry_insights": failure_industry_insights, # Use new key
                "web_sentiment": {
                    "original_snippets": web_sentiment_data_raw.get("snippets", []),
                    "overall_sentiment": web_sentiment_data_raw.get("overall_sentiment", {}),
                    "analyzed_snippets": analyzed_web_snippets,
                    "error": web_sentiment_data_raw.get("error")
                },
                "controversies": controversies_data,
                "analysis": {}
            }

            # --- Further Analysis ---
            logging.info("Performing final analysis (score, label, locations)...")
            # Use 'failed_startups' key from insights data for penalty calc
            specific_failures_found_list = failure_industry_insights.get("failed_startups", [])
            founder_data["analysis"]["reputation_score"] = analyzer.calculate_reputation_score(
                sentiment_scores=founder_data["web_sentiment"]["overall_sentiment"],
                failed_startups=specific_failures_found_list
            )
            founder_data["analysis"]["sentiment_label"] = founder_data["web_sentiment"]["overall_sentiment"].get('label', 'NEUTRAL')

            # Location Extraction
            texts_for_location = []
            if linked_data: texts_for_location.extend([linked_data.get("location"), linked_data.get("headline")])
            # Add failure detail snippets for location context if they exist
            if failure_industry_insights.get("failure_details"):
                for detail in failure_industry_insights["failure_details"]: texts_for_location.append(detail.get("snippet"))
            texts_for_location.extend(founder_data["web_sentiment"]["original_snippets"]) # Use original snippets
            texts_for_location_filtered = [str(text) for text in texts_for_location if text and isinstance(text, str)]
            founder_data["analysis"]["locations"] = analyzer.extract_potential_locations(texts_for_location_filtered)


            # --- Store the fetched data in cache BEFORE rendering ---
            logging.info(f"Storing results in cache with key: {cache_key}")
            cache.set(cache_key, founder_data, timeout=1800)

            # --- Log to CSV ---
            log_search_to_csv(founder_data, cache_status) # Log the data

        except Exception as e:
             # Handle potential errors during fetching/analysis
             logging.error(f"An error occurred during data fetching/analysis for query '{query}': {e}", exc_info=True) # Log full traceback
             # Return an error page or message
             return render_template('index.html', error=f"An error occurred while processing your request for '{query}'. Please try again later."), 500

        # --- Render Results Page ---
        logging.info(f"Rendering results page for query: '{query}'")
        return render_template('results.html', data=founder_data)


# --- API Endpoint (Optional - Update structure if used) ---
@app.route('/api/verify', methods=['GET'])
def api_verify():
    """Optional API endpoint - Returns cached data or placeholder."""
    # ... (keep previous implementation or update keys: 'failure_industry_insights') ...
    query = request.args.get('query')
    if not query: return jsonify({"error": "Query parameter is required"}), 400
    normalized_query = query.lower().strip()
    cache_key = f"founder_data_{normalized_query.replace(' ', '_').replace('/', '_')}"
    cached_data = cache.get(cache_key)
    if cached_data:
        logging.info(f"API Cache HIT for query: '{query}'")
        return jsonify(cached_data)
    else:
        logging.warning(f"API Cache MISS for query: '{query}'. Returning placeholder.")
        placeholder_data = { "query": query, "status": "Data not found in cache via API.", # ... add other keys with placeholder status ...
                           "failure_industry_insights": {"status": "Data not fetched via API"} }
        return jsonify(placeholder_data), 404


# --- Run the App ---
if __name__ == '__main__':
    logging.info("Starting Founder Verifier Flask application...")
    # Create dummy CSV file with header if it doesn't exist on startup
    if not os.path.isfile(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
         try:
             with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as csvfile:
                 writer = csv.DictWriter(csvfile, fieldnames=CSV_FIELDNAMES)
                 writer.writeheader()
             logging.info(f"Initialized empty log file: {CSV_FILE}")
         except Exception as init_csv_e:
             logging.error(f"Failed to initialize CSV log file {CSV_FILE}: {init_csv_e}")

    app.run(debug=True, host='0.0.0.0', port=5001) # debug=False for production