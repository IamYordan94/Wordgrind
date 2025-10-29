# WordGrind - Progressive Vocabulary Game

## Overview

WordGrind is a tier-based vocabulary learning game that challenges players to discover words progressively from 2-9 letters. The game features a subscription model with three tiers (Free, Premium, Lifetime) designed to reward dedicated learners. Players discover words through direct input and four engaging mini-games, building vocabulary systematically while tracking progress toward mastery.

## Product Model

### Tier System
- **Free Tier**: 20 words/day, 500 lifetime cap, 2-5 minute cooldowns, last 100 words in journal
- **Premium Tier**: $1.50/month via Stripe, 50 words/day, no cooldowns, unlimited journal with notes/export
- **Lifetime Tier**: Auto-unlocked at 58,535 discovered words (half the dictionary), premium features forever

### Monetization Strategy
- Monthly subscription via Stripe Payment Links
- No advertising or third-party monetization
- "Earn your mastery" approach rewards dedicated learners with lifetime free access

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application is built as a single-page web application using vanilla HTML, CSS, and JavaScript:

- **Static HTML Structure**: Multiple pages (index.html, home.html, vocabulary.html, upgrade.html)
- **Embedded CSS**: All styling contained within HTML files for simplicity and fast loading
- **Vanilla JavaScript**: Client-side game logic, tier management, and UI interactions
- **Mobile-First Design**: Responsive layout optimized for mobile, tablet, and desktop

### Tier Management System
The application manages tier state entirely on the client side using localStorage:

**Data Schema (localStorage: 'wordGrindTierData'):**
```javascript
{
  tier: 'free' | 'paid' | 'lifetime',
  dailyWordCount: number,          // Resets at midnight
  lifetimeWordCount: number,        // Total words ever discovered
  lastResetTimestamp: number,       // Midnight timestamp for daily reset
  subscriptionExpiry: number|null,  // For paid tier expiry
  dailyCap: 20 | 50,               // Based on tier
  lifetimeCap: 500 | 58535 | null, // Based on tier
  migrated: boolean,                // Legacy data migration flag
  createdAt: number                 // System initialization timestamp
}
```

**Core Functions:**
- `TierSystem.initializeTierSystem()` - Auto-initializes on page load, migrates legacy data
- `TierSystem.getUserTier()` - Returns current tier with expiry checking
- `TierSystem.canDiscoverWord()` - Pre-flight check for word discovery
- `TierSystem.incrementWordCount()` - Increments counters and checks caps
- `TierSystem.checkLifetimeUnlock()` - Auto-upgrades to lifetime at 58,535 words
- `TierSystem.upgradeToPaid(months)` - Handles subscription upgrades

### Cooldown System
Free tier users face cooldowns after using mini-games to encourage upgrade:

**Data Schema (localStorage: 'wordGrindCooldowns'):**
```javascript
{
  definitionMode: timestamp_when_available,
  hangman: timestamp_when_available,
  scramble: timestamp_when_available,
  mixMatch: timestamp_when_available
}
```

**Cooldown Durations:**
- Standard mini-games (Definition, Hangman, Scramble): 2 minutes
- Mix & Match: 5 minutes
- Paid tier: 30 seconds (moderate restriction)
- Lifetime tier: No cooldowns

### User Interface Design
The interface follows a dark theme aesthetic with tier-specific elements:

**Main Game Screen (index.html):**
- **Tier Badge**: Shows current subscription status (📋 Free, 💎 Premium, 🏆 Lifetime)
- **Progress Indicators**: Daily words used (X/20 or X/50) and lifetime progress (X/500 or X/58,535)
- **Word Discovery Input**: 
  - Free tier: Dropdown selector for word length (2-9 letters) + restricted input field
  - Paid/Lifetime tier: Universal input box accepting any 2-9 letter word
- **Mini-Game Buttons**: Definition, Hangman, Scramble, Mix & Match with cooldown timers (free tier only)
- **Navigation**: Home, Vocabulary, Upgrade, Rules

**Home Page (home.html):**
- Landing page with "Learn. Play. Earn your mastery." tagline
- Tier comparison cards (Free, Premium, Lifetime)
- Educational content explaining tier system and lifetime unlock
- Updated privacy policy (no advertising)

**Vocabulary Journal (vocabulary.html):**
- **Free Tier**: Last 100 discovered words, read-only with definitions
- **Paid/Lifetime Tier**: Complete word collection with search, filter, notes, CSV export
- Tier status badge and lifetime progress tracker
- Upgrade banner for free tier users

**Upgrade Page (upgrade.html):**
- Premium subscription pricing ($1.50/month)
- Feature comparison table (Free vs Paid vs Lifetime)
- Lifetime unlock explanation (58,535 words = free forever)
- Stripe Payment Link integration

### Word Discovery System
The game implements word discovery through direct input and mini-games:

**Word Input Flow:**
1. User selects word length (free tier) or types any word (paid/lifetime tier)
2. System checks `TierSystem.canDiscoverWord()` for daily/lifetime caps
3. Validates word length and checks against ENABLE1 dictionary (117,000+ words)
4. Fetches definition from Free Dictionary API
5. Calls `TierSystem.incrementWordCount()` on successful discovery
6. Stores word with definition in localStorage
7. Shows upgrade prompt if caps are hit

**Mini-Games (4 total):**
- **Definition Mode**: Reveals definition as hint for word discovery
- **Hangman**: Classic letter-guessing game with hangman visual
- **Scramble**: Unscramble letters to discover word
- **Mix & Match**: Match 5 words to their correct definitions

All mini-games respect tier system and cooldowns, fetching real definitions from API.

### Word Validation System
Uses the comprehensive ENABLE1 word database:

- **ENABLE1 Dictionary**: 117,000+ valid English words from 2-9 letters
  - 2-letter: 160 words
  - 3-letter: 1,421 words
  - 4-letter: 5,273 words
  - 5-letter: 10,230 words
  - 6-letter: 17,708 words
  - 7-letter: 23,870 words
  - 8-letter: 29,989 words
  - 9-letter: 28,419 words
- **Duplicate Prevention**: Prevents re-guessing of already discovered words
- **Performance Optimized**: Word data loaded from JSON file, cached in memory

## External Dependencies

### Payment Processing
- **Stripe Payment Links**: Simple subscription processing without backend
- Current link: `https://buy.stripe.com/6oUeVe2rO4MV9b9f8M2wU03`
- Used for: Monthly subscriptions and donation link in footer

### Word Dictionary Service
- **Free Dictionary API**: Real-time word definitions (api.dictionaryapi.dev)
- **Smart Caching**: Reduces API calls and improves performance
- **Fallback Handling**: Graceful error handling when definitions unavailable
- **Part of Speech Detection**: Extracts grammar information from API responses

### Browser Storage APIs
- **localStorage**: Tier data, discovered words, cooldowns, word notes
- **sessionStorage**: Temporary game state, service worker cleanup flags

## Recent Changes (October 2025)

### Major Rebuild: Level-Based → Tier-Based System
Transformed the game from a level-progression model to a subscription-based tier system:

**Removed:**
- Level unlock progression system
- AdSense integration and all advertising code
- Level-based UI controls and buttons
- 10-word browser limit system

**Added:**
- Three-tier subscription model (Free/Premium/Lifetime)
- Daily and lifetime word caps with auto-reset at midnight
- Cooldown timer system for free tier mini-games
- Upgrade page with Stripe payment integration
- Tier-specific vocabulary journal (100-word limit for free tier)
- Lifetime progress tracker toward 58,535-word milestone
- Universal word input for premium tiers
- Upgrade prompts at daily/lifetime caps

**Migration:**
- Legacy `wordleGrindProgress` data automatically migrated to new tier system
- Existing discovered words counted toward lifetime total
- Backward-compatible with existing localStorage data

## File Structure

```
/
├── index.html          - Main game with tier system, cooldowns, mini-games
├── home.html           - Landing page with tier marketing and About section
├── vocabulary.html     - Tier-based journal with notes/export for premium
├── upgrade.html        - Subscription page with Stripe payment link
├── words_data_final.json - ENABLE1 word database (117,000+ words)
└── replit.md          - This architecture document
```

## Future Considerations

### Potential Enhancements
- Backend API for subscription management and tier validation
- Cross-device sync for premium users (requires authentication)
- Streak tracking and daily challenges
- Word of the day feature
- Social sharing and leaderboards
- Analytics for player engagement tracking

### Security Considerations
- Client-side tier validation (can be bypassed - needs backend for production)
- localStorage tier data not tamper-resistant without encryption
- Stripe webhook integration for subscription status verification (requires backend)
- API rate limiting for definition fetching

## Testing & Debugging

### Debug Tools (Browser Console)
- `TierDebug.showStatus()` - Display current tier status
- `TierDebug.testUpgradePaid(months)` - Simulate paid upgrade
- `TierDebug.testLifetimeUnlock()` - Test lifetime unlock
- `CooldownDebug.showStatus()` - Display cooldown status
- `CooldownDebug.testSetCooldown(game, minutes)` - Test cooldowns

### Testing Scenarios
1. Free tier word discovery up to 20/day cap
2. Free tier cooldown enforcement on mini-games
3. 500 lifetime word cap → upgrade prompt
4. Paid tier upgrade → 50/day cap, no cooldowns
5. 58,535 lifetime words → auto-lifetime unlock
6. Journal access (100 words free, unlimited paid)
7. CSV export and notes (premium only)
