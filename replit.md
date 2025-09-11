# Progressive Wordle Grind

## Overview

Progressive Wordle Grind is a web-based word puzzle game inspired by Wordle that challenges players to discover all possible words starting from 2-letter combinations and progressively advancing through 9-letter words. Unlike traditional Wordle where players guess a single daily word, this game requires players to find every valid word of a given length before unlocking the next level. The game features a comprehensive progression system spanning 8 levels (2-letter through 9-letter words) with over 100,000+ words total, creating an engaging "grind" experience with clear advancement milestones.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application is built as a single-page web application using vanilla HTML, CSS, and JavaScript. The architecture follows a simple client-side approach with:

- **Static HTML Structure**: Single `index.html` file containing the complete game interface
- **Embedded CSS**: All styling is contained within the HTML file for simplicity and fast loading
- **Vanilla JavaScript**: Game logic, word validation, and UI interactions handled through plain JavaScript without external frameworks

### Game State Management
The application manages game state entirely on the client side:

- **Level Progression System**: Tracks current level (word length) and unlocks subsequent levels upon completion
- **Word Discovery Tracking**: Maintains a record of all discovered words for each level
- **Progress Persistence**: Uses browser localStorage to save game progress between sessions
- **Real-time Feedback**: Implements Wordle-style color-coded feedback (green, yellow, gray) for letter placement

### User Interface Design
The interface follows a dark theme aesthetic with:

- **Responsive Layout**: Centered container with max-width for optimal viewing on various screen sizes
- **Game Information Panel**: Displays current level, progress statistics, and completion status
- **Input System**: Text input field for word guesses with immediate validation feedback
- **Progress Visualization**: Shows discovered words and completion percentage for each level

### Word Validation System
The game implements a comprehensive word validation approach using the ENABLE1 word database:

- **ENABLE1 Dictionary Integration**: Uses the comprehensive ENABLE1 word database containing over 100,000+ valid English words from 2-9 letters
- **Length-based Filtering**: Supports 8 progression levels covering 2-letter through 9-letter words (28,419 nine-letter words included)
- **Duplicate Prevention**: Prevents re-guessing of already discovered words
- **Completion Detection**: Automatically advances to next level when all words of current length are found
- **Performance Optimized**: Enhanced caching system and Service Worker management for smooth gameplay

## External Dependencies

### Word Dictionary Service
The application requires access to a word dictionary or vocabulary database to:

- Validate player guesses against legitimate English words
- Generate the complete set of valid words for each length category
- Ensure consistent word standards across all levels

### Browser Storage APIs
Utilizes browser-native storage capabilities:

- **localStorage**: For persisting game progress, discovered words, and current level between sessions
- **sessionStorage**: For temporary game state during active play sessions

### Potential Future Integrations
The architecture supports future enhancement through:

- **Analytics Services**: For tracking player engagement and completion rates
- **Social Features**: Integration with social media APIs for sharing progress
- **Leaderboard Systems**: Connection to backend services for competitive features
- **Word Database APIs**: Integration with comprehensive dictionary services for expanded word sets