#!/usr/bin/env python3
import json

# Read the word list
print("Reading ENABLE1 word list...")
with open('attached_assets/enable1_1757581498164.txt', 'r') as f:
    all_words = [word.strip().lower() for word in f.readlines()]

print(f"Total words in ENABLE1: {len(all_words)}")

# Organize words by length (2-9 letters only)
words_by_length = {}

for word in all_words:
    length = len(word)
    # Only include words with 2-9 letters
    if 2 <= length <= 9:
        if str(length) not in words_by_length:
            words_by_length[str(length)] = []
        
        # Add word with basic structure (we'll keep definitions simple for now)
        words_by_length[str(length)].append({
            "word": word,
            "pos": "unknown",  # We could enhance this later with POS tagging
            "definition": "A valid English word - definition not available"
        })

# Print statistics
print("\nWord count by length:")
total_words = 0
for length in sorted(words_by_length.keys(), key=int):
    count = len(words_by_length[length])
    total_words += count
    print(f"  {length}-letter words: {count:,}")

print(f"\nTotal words (2-9 letters): {total_words:,}")

# Save to new words_data.json
print("\nSaving to words_data.json...")
with open('words_data_new.json', 'w') as f:
    json.dump(words_by_length, f, indent=2)

print("✅ Complete! New word database saved to words_data_new.json")