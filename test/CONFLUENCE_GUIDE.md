# Environment Banner - Quick Start Guide

**Prevent accidental use of non-production environments with production data.**

---

## TL;DR - Quick Setup

### Python (Flask/FastAPI/Django)
```python
from envbanner import flask as envbanner_flask  # or: from envbanner import ASGIBannerMiddleware
envbanner_flask(app, position='bottom', text="DON'T USE REAL DATA - Dev Environment", show_host=False)
```

### Node.js (Express)
```javascript
const envBanner = require('env-banner-node');
app.use(envBanner({position: 'bottom', text: "DON'T USE REAL DATA - Dev Environment", showHost: false}));
```

**Default:** Bottom banner, auto-detects environment, shows hostname.

---

## Installation

### Python
```bash
pip install env-banner
# OR from git:
pip install "git+https://github.com/sagearbor/env-banner-python.git"
```

### Node.js
```bash
npm install env-banner-node
# OR from git:
npm install git+https://github.com/sagearbor/env-banner-node.git
```

---

## Basic Integration

### Python - Flask
```python
from flask import Flask
from envbanner import flask as envbanner_flask

app = Flask(__name__)

# Apply right after app creation, before routes
envbanner_flask(app, position='bottom', text="DON'T USE REAL DATA - Dev Environment", show_host=False)

@app.route('/')
def index():
    return '<h1>Hello World</h1>'
```

### Python - FastAPI
```python
from fastapi import FastAPI
from envbanner import ASGIBannerMiddleware

app = FastAPI()

# Apply right after app creation
app.add_middleware(
    ASGIBannerMiddleware,
    position='bottom',
    text="DON'T USE REAL DATA - Dev Environment",
    show_host=False
)

@app.get('/')
def index():
    return {"message": "Hello World"}
```

### Python - Django
```python
# settings.py
MIDDLEWARE = [
    'envbanner.middleware.WSGIBannerMiddleware',  # Add at top
    'django.middleware.security.SecurityMiddleware',
    # ... rest of middleware
]

# To customize, you'll need to wrap it:
# See README.md for advanced Django configuration
```

### Node.js - Express
```javascript
const express = require('express');
const envBanner = require('env-banner-node');

const app = express();

// Apply environment banner middleware right after security (before everything else)
console.log('[DEBUG] env-banner-node loaded:', typeof envBanner);
app.use(envBanner({
  position: 'bottom', // 'diagonal',
  text: "DON'T USE REAL DATA - Dev Environment",
  showHost: false
})); // Banner at bottom to avoid navbar collision
console.log('[DEBUG] env-banner-node middleware applied');

app.get('/', (req, res) => {
  res.send('<h1>Hello World</h1>');
});

app.listen(3000);
```

---

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `position` | string | `'bottom'` | Where to show banner (see positions below) |
| `text` | string | Auto (e.g. "DEV") | Custom text to display |
| `background` | string | Auto (red/amber) | Background color (hex: `#ef4444`) |
| `color` | string | Auto (white) | Text color (hex: `#ffffff`) |
| `showHost` / `show_host` | boolean | `true` | Show hostname (e.g. "• localhost:5000") |
| `opacity` | number | `1.0` (bars), `0.5` (diagonal) | Transparency (0.0-1.0) |

**Note:** Python uses snake_case (`show_host`), Node.js uses camelCase (`showHost`).

---

## Position Options

| Position | Description | Visual |
|----------|-------------|--------|
| `'bottom'` | Full-width bar at bottom **(DEFAULT)** | `[=========]` at bottom |
| `'top'` | Full-width bar at top | `[=========]` at top |
| `'diagonal'` or `'diagonal-bltr'` | Diagonal stripe (/) | `/` across page |
| `'diagonal-tlbr'` | Diagonal stripe (\) | `\` across page |
| `'top-right'` | Corner ribbon | Small ribbon at ⌝ |
| `'top-left'` | Corner ribbon | Small ribbon at ⌜ |
| `'bottom-right'` | Corner ribbon | Small ribbon at ⌟ |
| `'bottom-left'` | Corner ribbon | Small ribbon at ⌞ |

**Recommendation:** Use `'bottom'` or `'diagonal'` for maximum visibility.

---

## Environment Detection

The banner auto-detects the environment using this logic:

1. **Check environment variable:** `APP_ENV` (or `NODE_ENV` for Node.js)
2. **Check hostname/URL patterns:**
   - `localhost`, `127.0.0.1`, `*.local` → DEV (red banner)
   - `*.dev.*`, `*-dev-*` → DEV (red banner)
   - `*.staging.*`, `*.stg.*` → STAGING (amber banner)
   - `*.val.*`, `*-preprod-*` → STAGING (amber banner)
3. **Default:** DEV (red banner) if uncertain

**Production:** Set `APP_ENV=production` or `NODE_ENV=production` → **No banner shown**

---

## Common Configurations

### 1. Minimal (default behavior)
```python
# Python
envbanner_flask(app)
```
```javascript
// Node.js
app.use(envBanner());
```
**Result:** Bottom bar, shows "DEV • localhost:5000"

---

### 2. Custom text, no hostname
```python
# Python
envbanner_flask(app,
    text="DON'T USE REAL DATA",
    show_host=False
)
```
```javascript
// Node.js
app.use(envBanner({
  text: "DON'T USE REAL DATA",
  showHost: false
}));
```
**Result:** Bottom bar, shows "DON'T USE REAL DATA"

---

### 3. Diagonal stripe (maximum visibility)
```python
# Python
envbanner_flask(app,
    position='diagonal',
    text="TEST ENVIRONMENT",
    opacity=0.7
)
```
```javascript
// Node.js
app.use(envBanner({
  position: 'diagonal',
  text: "TEST ENVIRONMENT",
  opacity: 0.7
}));
```
**Result:** Diagonal stripe across page with 70% opacity

---

### 4. Top-right corner (subtle)
```python
# Python
envbanner_flask(app, position='top-right')
```
```javascript
// Node.js
app.use(envBanner({ position: 'top-right' }));
```
**Result:** Small ribbon in top-right corner

---

### 5. Custom colors (e.g., purple for QA)
```python
# Python
envbanner_flask(app,
    text="QA ENVIRONMENT",
    background="#9333ea",
    color="#ffffff"
)
```
```javascript
// Node.js
app.use(envBanner({
  text: "QA ENVIRONMENT",
  background: "#9333ea",
  color: "#ffffff"
}));
```
**Result:** Bottom bar with purple background, white text

---

## Production Deployment

**Critical:** Set the environment variable to disable the banner:

### Docker
```dockerfile
ENV APP_ENV=production
# or for Node.js:
ENV NODE_ENV=production
```

### Kubernetes
```yaml
env:
  - name: APP_ENV
    value: "production"
# or for Node.js:
  - name: NODE_ENV
    value: "production"
```

### Environment Files
```bash
# .env
APP_ENV=production
```

**Verify:** Banner should NOT appear in production.

---

## Testing

### Python
```bash
# Install test server
pip install flask

# Run test server
python test/flask-app.py

# Visit http://localhost:5000
# Edit test/flask-app.py to try different positions
```

### Node.js
```bash
# Run test server
node test/express-app.js

# Visit http://localhost:3000
# Edit test/express-app.js to try different positions
```

---

## Troubleshooting

### Banner doesn't appear
- Check `APP_ENV` / `NODE_ENV` is NOT set to "production"
- Verify middleware is loaded before routes
- Check browser console for errors
- Ensure response is `text/html` (JSON responses are ignored)

### Banner appears in production
- **Fix immediately!** Set `APP_ENV=production` or `NODE_ENV=production`
- Verify environment variable is set: `echo $APP_ENV`
- Restart your application after setting env var

### Wrong position
- Check spelling of position parameter
- Python: Use `position='bottom'`
- Node.js: Use `position: 'bottom'` (object syntax)

### Text not showing correctly
- Use `text` parameter to customize
- Set `show_host=False` (Python) or `showHost: false` (Node.js) to hide hostname

---

## Security Notes

✅ **Safe:** All user-facing text is HTML-escaped
✅ **Safe:** CSS is generated server-side (no user input)
✅ **Safe:** Banner only shows in non-production environments
⚠️ **Note:** Configuration options (text, colors) should only be set by developers in code, not from user input

---

## Support

- **Python Repo:** https://github.com/sagearbor/env-banner-python
- **Node.js Repo:** https://github.com/sagearbor/env-banner-node
- **Issues:** File on the respective GitHub repo

---

## Quick Reference Card

```python
# PYTHON - Most Common Setup
from envbanner import flask as envbanner_flask
envbanner_flask(app, position='bottom', text="DON'T USE REAL DATA", show_host=False)
```

```javascript
// NODE.JS - Most Common Setup
const envBanner = require('env-banner-node');
app.use(envBanner({
  position: 'bottom',
  text: "DON'T USE REAL DATA",
  showHost: false
}));
```

**Production:** `APP_ENV=production` or `NODE_ENV=production` → No banner

---

*Last updated: 2025-01-20 | Version: 0.1.0*
