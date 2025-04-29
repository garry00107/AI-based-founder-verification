# analyzer.py
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- VADER Lexicon Download Logic ---
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    logging.info("Downloading VADER lexicon...")
    try:
         nltk.download('vader_lexicon')
         logging.info("VADER lexicon downloaded successfully.")
    except Exception as download_e:
         logging.error(f"Failed to download VADER lexicon: {download_e}")
         logging.error("Sentiment analysis will likely fail. Please try downloading manually:")
         logging.error(">>> import nltk")
         logging.error(">>> nltk.download('vader_lexicon')")
except Exception as e:
     logging.warning(f"Could not check/download VADER lexicon: {e}. Sentiment analysis might fail.")
     logging.info("Attempting to proceed anyway...")
# --- End VADER Download Logic ---

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using VADER.
    Returns a dictionary with positive, negative, neutral, and compound scores.
    """
    if not text or not isinstance(text, str):
        return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0, 'label': 'NEUTRAL'}

    try:
        analyzer = SentimentIntensityAnalyzer()
        vs = analyzer.polarity_scores(text)

        # Determine label based on compound score
        if vs['compound'] >= 0.05:
            vs['label'] = 'POSITIVE'
        elif vs['compound'] <= -0.05:
            vs['label'] = 'NEGATIVE'
        else:
            vs['label'] = 'NEUTRAL'
        return vs
    except Exception as e:
        logging.error(f"Error during sentiment analysis: {e}")
        # Return neutral sentiment in case of error
        return {'neg': 0.0, 'neu': 1.0, 'pos': 0.0, 'compound': 0.0, 'label': 'NEUTRAL'}


def extract_potential_locations(text_list):
    """
    Placeholder function to simulate extracting geographical locations from text.
    Improved slightly to handle None and filter duplicates better.
    """
    locations = []
    # Expanded patterns slightly
    patterns = [
        r'\b(San Francisco|New York|NYC|London|Berlin|Paris|Tokyo|Singapore|Bangalore|Mumbai|Delhi|Austin|Seattle)\b',
        r'\b(USA|UK|United Kingdom|Germany|France|Japan|India|California|CA|NY|Texas|TX|Washington|WA)\b'
    ]
    # Filter out None values and join
    valid_texts = [str(t) for t in text_list if t]
    combined_text = " ".join(valid_texts)
    if not combined_text:
        return [{"name": "Default Location (Unknown)", "lat": 37.4419, "lon": -122.1430}] # Palo Alto

    found_places = set() # Use a set to store unique location names found

    for pattern in patterns:
        try:
            matches = re.findall(pattern, combined_text, re.IGNORECASE)
            for match in matches:
                loc_data = None
                match_lower = match.lower()
                # More robust mapping needed for production
                if match_lower in ["san francisco", "california", "ca", "sf"]:
                    loc_name = "San Francisco, CA"
                    if loc_name not in found_places:
                        loc_data = {"name": loc_name, "lat": 37.7749, "lon": -122.4194}
                elif match_lower in ["new york", "ny", "nyc"]:
                    loc_name = "New York, NY"
                    if loc_name not in found_places:
                        loc_data = {"name": loc_name, "lat": 40.7128, "lon": -74.0060}
                elif match_lower in ["london", "uk", "united kingdom"]:
                    loc_name = "London, UK"
                    if loc_name not in found_places:
                         loc_data = {"name": loc_name, "lat": 51.5074, "lon": -0.1278}
                elif match_lower == "berlin":
                     loc_name = "Berlin, Germany"
                     if loc_name not in found_places:
                        loc_data = {"name": loc_name, "lat": 52.5200, "lon": 13.4050}
                elif match_lower == "bangalore":
                     loc_name = "Bangalore, India"
                     if loc_name not in found_places:
                        loc_data = {"name": loc_name, "lat": 12.9716, "lon": 77.5946}
                elif match_lower in ["austin", "texas", "tx"]:
                     loc_name = "Austin, TX"
                     if loc_name not in found_places:
                        loc_data = {"name": loc_name, "lat": 30.2672, "lon": -97.7431}
                elif match_lower in ["seattle", "washington", "wa"]:
                     loc_name = "Seattle, WA"
                     if loc_name not in found_places:
                         loc_data = {"name": loc_name, "lat": 47.6062, "lon": -122.3321}
                # Add more mappings...

                if loc_data:
                     locations.append(loc_data)
                     found_places.add(loc_data["name"]) # Add found name to set
        except Exception as regex_e:
            logging.error(f"Error during regex location extraction: {regex_e} on pattern: {pattern}")


    # Add a default if none found after searching
    if not locations:
         # Palo Alto as default
         locations.append({"name": "Default Location (Palo Alto, CA)", "lat": 37.4419, "lon": -122.1430})

    logging.info(f"Extracted locations: {locations}")
    return locations


def calculate_reputation_score(sentiment_scores, failed_startups=None):
    """
    Calculates a reputation score based ONLY on web sentiment,
    but is penalized if Failory found specific failure details.
    Score calculation remains the same as before.
    """
    if failed_startups is None:
        failed_startups = []

    # Calculate base score from sentiment
    if not sentiment_scores:
        base_score = 50 # Neutral default
    else:
        compound_score = sentiment_scores.get('compound', 0.0)
        base_score = ((compound_score + 1) / 2) * 100
        base_score = max(0, min(100, base_score)) # Clamp to 0-100

    logging.debug(f"Base score from sentiment: {base_score:.2f}")

    # Apply Penalty ONLY if specific failures were scraped (e.g., from Failory check)
    penalty_factor = 1.0
    num_failures = len(failed_startups) # This list comes from the 'failed_startups' key which should ONLY be populated if specific scraping found something

    if num_failures > 0:
        logging.info(f"Applying penalty: Found {num_failures} associated failure(s) potentially via Failory.")
        penalty_reduction = 0.30 + (min(num_failures - 1, 2) * 0.05)
        penalty_factor = 1.0 - penalty_reduction
        logging.debug(f"Penalty factor applied: {penalty_factor:.2f}")
    else:
        logging.debug("No specific failures found from scraping source, no penalty applied to score.")

    final_score = base_score * penalty_factor
    final_score = max(0, min(100, final_score)) # Clamp final score

    logging.info(f"Final reputation score: {round(final_score)}")
    return round(final_score)