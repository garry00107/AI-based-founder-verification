# nltk_downloader.py
import nltk
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_nltk_data():
    """Download required NLTK data for the application."""
    try:
        # Try to find vader_lexicon
        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
            logging.info("VADER lexicon already available.")
            return True
        except LookupError:
            logging.info("VADER lexicon not found. Downloading...")
            
            # Download vader_lexicon
            nltk.download('vader_lexicon', quiet=True)
            logging.info("VADER lexicon downloaded successfully.")
            return True
            
    except Exception as e:
        logging.error(f"Failed to download NLTK data: {e}")
        return False

def ensure_nltk_data():
    """Ensure NLTK data is available, with fallback for serverless environments."""
    try:
        # Try to download
        if download_nltk_data():
            return True
    except Exception as e:
        logging.warning(f"NLTK download failed: {e}")
    
    # Fallback: try to use cached data or continue without it
    try:
        from nltk.sentiment.vader import SentimentIntensityAnalyzer
        # Try to create analyzer to see if it works
        analyzer = SentimentIntensityAnalyzer()
        logging.info("VADER analyzer created successfully (using cached data)")
        return True
    except Exception as e:
        logging.error(f"VADER analyzer creation failed: {e}")
        return False

# Run on import
if __name__ == "__main__":
    ensure_nltk_data()
