# WordGrind - Progressive Vocabulary Game

A tier-based vocabulary learning game that challenges players to discover words progressively from 2-9 letters. Build your vocabulary through direct input and engaging mini-games while tracking your progress toward mastery.

## 🎮 Features

- **Progressive Learning**: Discover words from 2 to 9 letters
- **Tier System**: Free, Premium, and Lifetime tiers with different features
- **Mini-Games**: Definition Mode, Hangman, Scramble, and Mix & Match
- **Vocabulary Journal**: Track all discovered words with definitions
- **Offline Support**: Progressive Web App (PWA) that works offline
- **No Ads**: Clean, focused learning experience

## 🚀 Getting Started

### Local Development

Since this is a static site, you can run it locally using any HTTP server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server -p 8000

# Using PHP
php -S localhost:8000
```

Then open `http://localhost:8000` in your browser.

### Deploy to Vercel

1. Push your code to GitHub
2. Import your repository in [Vercel](https://vercel.com)
3. Vercel will automatically detect the static site and deploy it
4. Your app will be live!

## 📋 Tier System

### Free Tier
- 20 words per day
- 500 lifetime word limit
- 2-5 minute cooldowns on mini-games
- Last 100 words in vocabulary journal

### Premium Tier ($0.50/month)
- 50 words per day
- No daily or lifetime caps
- Zero cooldowns—play instantly
- Full vocabulary journal with search & export
- Advanced statistics and insights

### Lifetime Tier (Earned Free)
- Unlock at 58,535 words discovered
- Premium features forever—free!
- Badge of mastery achievement
- Reward for discovering half of English

## 🏗️ Architecture

### Frontend
- **Pure HTML/CSS/JavaScript**: No build process required
- **Static Files**: All pages are standalone HTML files
- **localStorage**: Client-side data persistence
- **PWA**: Progressive Web App with offline support

### External Services
- **Stripe Payment Links**: Subscription processing
- **Free Dictionary API**: Word definitions (api.dictionaryapi.dev)
- **ENABLE1 Dictionary**: 117,000+ valid English words

## 📁 File Structure

```
/
├── index.html          - Main game with tier system, cooldowns, mini-games
├── home.html           - Landing page with tier marketing and About section
├── vocabulary.html     - Tier-based journal with notes/export for premium
├── upgrade.html         - Subscription page with Stripe payment link
├── words_data_final.json - ENABLE1 word database (117,000+ words)
├── vercel.json         - Vercel deployment configuration
├── .gitignore          - Git ignore rules
└── README.md           - This file
```

## 🔧 Configuration

### Vercel Deployment

The `vercel.json` file is already configured for static site deployment. No additional setup needed.

### Stripe Integration

Update the Stripe payment link in:
- `upgrade.html` (line 298)
- `home.html` (line 497)
- `vocabulary.html` (line 724)

Stripe Payment Link: `https://buy.stripe.com/9B64gA3vSbbj8755yc2wU04`

## 🧪 Testing

### Debug Tools (Browser Console)

```javascript
// Display current tier status
TierDebug.showStatus()

// Simulate paid upgrade
TierDebug.testUpgradePaid(months)

// Test lifetime unlock
TierDebug.testLifetimeUnlock()

// Display cooldown status
CooldownDebug.showStatus()

// Test cooldowns
CooldownDebug.testSetCooldown(game, minutes)
```

## 📝 License

This project is private and proprietary.

## 👤 Author

Made by Yo ✌

---

**Note**: This is a client-side only application. Tier validation happens on the client side and can be bypassed. For production use, consider implementing backend validation for subscription status.

