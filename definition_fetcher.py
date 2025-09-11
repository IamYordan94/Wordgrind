#!/usr/bin/env python3
"""
Definition Fetcher for Word Game Database

This script fetches real definitions for placeholder words in words_data_final.json
using the Free Dictionary API. It includes rate limiting, progress tracking,
error handling, and backup functionality.

Usage: python definition_fetcher.py [--resume] [--test-mode]
"""

import json
import time
import requests
import shutil
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('definition_fetcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DefinitionFetcher:
    def __init__(self, data_file='words_data_final.json', backup_dir='backups', 
                 progress_file='fetch_progress.json', test_mode=False):
        self.data_file = data_file
        self.backup_dir = Path(backup_dir)
        self.progress_file = progress_file
        self.test_mode = test_mode
        self.api_url = "https://api.dictionaryapi.dev/api/v2/entries/en/{}"
        self.rate_limit = 1.5  # seconds between requests
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'WordGameDefinitionFetcher/1.0'})
        
        # Statistics
        self.stats = {
            'total_processed': 0,
            'successful_updates': 0,
            'api_failures': 0,
            'network_errors': 0,
            'start_time': None,
            'last_save': None
        }
        
        # Create directories
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self) -> str:
        """Create a timestamped backup of the original file."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = self.backup_dir / f"words_data_final_{timestamp}.json"
        shutil.copy2(self.data_file, backup_path)
        logger.info(f"Backup created: {backup_path}")
        return str(backup_path)
    
    def load_data(self) -> Dict:
        """Load the words data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded data from {self.data_file}")
            return data
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise
    
    def save_data(self, data: Dict) -> None:
        """Save the updated words data to JSON file."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.stats['last_save'] = datetime.now()
            logger.info(f"Data saved to {self.data_file}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
            raise
    
    def load_progress(self) -> Dict:
        """Load progress from previous session."""
        try:
            if Path(self.progress_file).exists():
                with open(self.progress_file, 'r') as f:
                    progress = json.load(f)
                logger.info(f"Loaded progress: {progress.get('processed_count', 0)} words processed")
                return progress
        except Exception as e:
            logger.warning(f"Could not load progress file: {e}")
        return {'processed_words': set(), 'processed_count': 0}
    
    def save_progress(self, progress: Dict) -> None:
        """Save current progress."""
        try:
            # Convert set to list for JSON serialization
            progress_to_save = progress.copy()
            if 'processed_words' in progress_to_save:
                progress_to_save['processed_words'] = list(progress['processed_words'])
            
            with open(self.progress_file, 'w') as f:
                json.dump(progress_to_save, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save progress: {e}")
    
    def fetch_definition(self, word: str) -> Optional[Dict]:
        """
        Fetch definition for a word from Free Dictionary API.
        
        Returns:
            Dict with 'definition' and 'pos' keys, or None if not found
        """
        try:
            url = self.api_url.format(word.lower())
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and isinstance(data, list) and len(data) > 0:
                    word_data = data[0]
                    
                    # Extract first definition and part of speech
                    if 'meanings' in word_data and word_data['meanings']:
                        first_meaning = word_data['meanings'][0]
                        pos = first_meaning.get('partOfSpeech', 'unknown')
                        
                        if 'definitions' in first_meaning and first_meaning['definitions']:
                            definition = first_meaning['definitions'][0].get('definition', '')
                            
                            return {
                                'definition': definition,
                                'pos': pos
                            }
            
            elif response.status_code == 404:
                logger.debug(f"Word not found in dictionary: {word}")
                return None
            
            else:
                logger.warning(f"API returned {response.status_code} for word: {word}")
                self.stats['api_failures'] += 1
                return None
                
        except requests.RequestException as e:
            logger.warning(f"Network error for word '{word}': {e}")
            self.stats['network_errors'] += 1
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching definition for '{word}': {e}")
            return None
    
    def get_placeholder_words(self, data: Dict) -> List[Tuple[str, str, int]]:
        """
        Get all words with placeholder definitions.
        
        Returns:
            List of tuples: (word, length_key, index_in_list)
        """
        placeholder_words = []
        placeholder_definition = "A valid English word - definition not available"
        
        for length_key, words_list in data.items():
            for index, word_entry in enumerate(words_list):
                if word_entry.get('definition') == placeholder_definition:
                    placeholder_words.append((word_entry['word'], length_key, index))
        
        logger.info(f"Found {len(placeholder_words)} words with placeholder definitions")
        return placeholder_words
    
    def print_statistics(self) -> None:
        """Print current statistics."""
        if self.stats['start_time']:
            elapsed = datetime.now() - self.stats['start_time']
            hours, remainder = divmod(elapsed.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            logger.info("=== STATISTICS ===")
            logger.info(f"Runtime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}")
            logger.info(f"Words processed: {self.stats['total_processed']:,}")
            logger.info(f"Successful updates: {self.stats['successful_updates']:,}")
            logger.info(f"API failures: {self.stats['api_failures']:,}")
            logger.info(f"Network errors: {self.stats['network_errors']:,}")
            
            if self.stats['total_processed'] > 0:
                success_rate = (self.stats['successful_updates'] / self.stats['total_processed']) * 100
                logger.info(f"Success rate: {success_rate:.1f}%")
                
                if elapsed.total_seconds() > 0:
                    words_per_hour = (self.stats['total_processed'] / elapsed.total_seconds()) * 3600
                    logger.info(f"Processing rate: {words_per_hour:.1f} words/hour")
            logger.info("==================")
    
    def run(self, resume: bool = False) -> None:
        """Main execution method."""
        try:
            self.stats['start_time'] = datetime.now()
            logger.info(f"Starting definition fetcher {'(RESUME MODE)' if resume else '(FULL RUN)'}")
            logger.info(f"Test mode: {'ON' if self.test_mode else 'OFF'}")
            
            # Create backup unless resuming
            if not resume:
                self.create_backup()
            
            # Load data and progress
            data = self.load_data()
            progress = self.load_progress() if resume else {'processed_words': set(), 'processed_count': 0}
            
            # Convert progress words back to set
            if 'processed_words' in progress and isinstance(progress['processed_words'], list):
                progress['processed_words'] = set(progress['processed_words'])
            
            placeholder_words = self.get_placeholder_words(data)
            
            # Filter out already processed words if resuming
            if resume and progress['processed_words']:
                original_count = len(placeholder_words)
                placeholder_words = [(w, lk, idx) for w, lk, idx in placeholder_words 
                                   if w not in progress['processed_words']]
                logger.info(f"Resuming: {original_count - len(placeholder_words)} words already processed")
            
            total_to_process = len(placeholder_words)
            logger.info(f"Words to process: {total_to_process:,}")
            
            # Limit for test mode
            if self.test_mode:
                placeholder_words = placeholder_words[:50]  # Only process first 50 words
                logger.info(f"Test mode: limiting to {len(placeholder_words)} words")
            
            # Process words
            save_interval = 100  # Save progress every 100 words
            last_save_count = 0
            
            for i, (word, length_key, word_index) in enumerate(placeholder_words, 1):
                try:
                    logger.info(f"[{i}/{len(placeholder_words)}] Processing: {word}")
                    
                    # Fetch definition
                    result = self.fetch_definition(word)
                    
                    if result and result.get('definition'):
                        # Update the word entry
                        data[length_key][word_index]['definition'] = result['definition']
                        data[length_key][word_index]['pos'] = result['pos']
                        
                        self.stats['successful_updates'] += 1
                        logger.info(f"✓ Updated {word}: {result['pos']} - {result['definition'][:100]}...")
                    else:
                        logger.info(f"✗ No definition found for: {word}")
                    
                    # Track progress
                    progress['processed_words'].add(word)
                    progress['processed_count'] += 1
                    self.stats['total_processed'] += 1
                    
                    # Periodic saves and statistics
                    if self.stats['total_processed'] - last_save_count >= save_interval:
                        self.save_data(data)
                        self.save_progress(progress)
                        self.print_statistics()
                        last_save_count = self.stats['total_processed']
                    
                    # Rate limiting
                    time.sleep(self.rate_limit)
                    
                except KeyboardInterrupt:
                    logger.info("Interrupted by user. Saving progress...")
                    break
                except Exception as e:
                    logger.error(f"Error processing word '{word}': {e}")
                    continue
            
            # Final save
            logger.info("Saving final data...")
            self.save_data(data)
            self.save_progress(progress)
            
            # Final statistics
            self.print_statistics()
            
            logger.info("Definition fetching completed!")
            
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Fetch real definitions for placeholder words')
    parser.add_argument('--resume', action='store_true', 
                       help='Resume from previous session')
    parser.add_argument('--test-mode', action='store_true',
                       help='Test mode - only process first 50 words')
    
    args = parser.parse_args()
    
    fetcher = DefinitionFetcher(test_mode=args.test_mode)
    
    try:
        fetcher.run(resume=args.resume)
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()