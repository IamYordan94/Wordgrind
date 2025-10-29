
import json

# Load the word data
with open('words_data_final.json', 'r') as f:
    data = json.load(f)

# Count words by level
total = 0
for level, words in sorted(data.items()):
    count = len(words)
    total += count
    letter_count = int(level)
    print(f"Level {letter_count-1} ({level}-letter words): {count:,} words")

print(f"\n{'='*50}")
print(f"TOTAL WORDS IN DATABASE: {total:,}")
print(f"{'='*50}")
