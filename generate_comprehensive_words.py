
#!/usr/bin/env python3
"""
Script to generate comprehensive English word dictionary for Progressive Wordle Game
Uses NLTK's word corpus and adds educational definitions
"""

import json
import nltk
from nltk.corpus import words, wordnet
from collections import defaultdict

try:
    # Download required NLTK data
    nltk.download('words', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
except:
    print("Installing NLTK data...")

def get_definition(word):
    """Get definition from WordNet"""
    synsets = wordnet.synsets(word)
    if synsets:
        # Get the most common definition
        return synsets[0].definition()
    return "A valid English word - definition not available"

def get_pos_tag(word):
    """Get part of speech"""
    synsets = wordnet.synsets(word)
    if synsets:
        pos = synsets[0].pos()
        pos_mapping = {
            'n': 'noun',
            'v': 'verb', 
            'a': 'adjective',
            'r': 'adverb',
            's': 'adjective'
        }
        return pos_mapping.get(pos, 'unknown')
    return 'unknown'

def filter_word(word):
    """Filter out unwanted words"""
    # Keep only alphabetic characters
    if not word.isalpha():
        return False
    
    # Filter out very short words that aren't useful
    if len(word) < 2:
        return False
        
    # Filter out common abbreviations and acronyms
    if word.isupper() and len(word) > 1:
        return False
    
    # Filter out words with apostrophes, hyphens, etc.
    if any(char in word for char in ["'", "-", ".", " "]):
        return False
        
    return True

def generate_word_dictionary(max_length=8):
    """Generate comprehensive word dictionary"""
    
    # Get English words from NLTK
    english_words = set(words.words())
    
    # Organize by length
    words_by_length = defaultdict(list)
    
    print(f"Processing {len(english_words)} English words...")
    
    processed = 0
    for word in english_words:
        if filter_word(word) and len(word) <= max_length:
            word_lower = word.lower()
            length = len(word_lower)
            
            # Get definition and POS
            definition = get_definition(word_lower)
            pos = get_pos_tag(word_lower)
            
            words_by_length[length].append({
                "word": word_lower,
                "pos": pos,
                "definition": definition
            })
            
        processed += 1
        if processed % 1000 == 0:
            print(f"Processed {processed} words...")
    
    # Sort words within each length group
    for length in words_by_length:
        words_by_length[length].sort(key=lambda x: x["word"])
    
    return dict(words_by_length)

if __name__ == "__main__":
    print("Generating comprehensive word dictionary...")
    
    # Generate the dictionary
    word_dict = generate_word_dictionary(max_length=8)
    
    # Print statistics
    total_words = sum(len(words) for words in word_dict.values())
    print(f"\nGenerated dictionary with {total_words} words:")
    for length, words in sorted(word_dict.items()):
        print(f"  {length}-letter words: {len(words)}")
    
    # Save to JSON file
    with open('words_data.json', 'w', encoding='utf-8') as f:
        json.dump(word_dict, f, indent=2, ensure_ascii=False)
    
    print(f"\nDictionary saved to words_data.json")
    
    # Show some examples
    print("\nExample words:")
    for length in sorted(word_dict.keys())[:3]:
        print(f"\n{length}-letter words (first 5):")
        for word_obj in word_dict[length][:5]:
            print(f"  {word_obj['word']}: {word_obj['definition'][:50]}...")
