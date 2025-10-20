#!/usr/bin/env python3
# test/flask-app.py
# Simple Flask test server for env-banner

import sys
import os

# Add parent directory to path to import envbanner
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
import envbanner

app = Flask(__name__)
PORT = 5000

# Test different banner configurations
# Uncomment ONE of the following options, then restart the server (Ctrl+C and run again):

# 1. Diagonal banner - Bottom-Left to Top-Right (/) - DEFAULT diagonal direction
envbanner.flask(app, position='diagonal')
# or explicitly:
# envbanner.flask(app, position='diagonal-bltr')

# 2. Diagonal banner - Top-Left to Bottom-Right (\)
# envbanner.flask(app, position='diagonal-tlbr')

# 3. Diagonal with custom opacity
# envbanner.flask(app, position='diagonal', opacity=0.7)

# 4. Top-right corner ribbon
# envbanner.flask(app, position='top-right')

# 5. Top bar
# envbanner.flask(app, position='top')

# 6. Bottom bar (DEFAULT if no position specified)
# envbanner.flask(app)  # No position = bottom bar by default
# or explicitly:
# envbanner.flask(app, position='bottom')

# 7. Custom text and colors
# envbanner.flask(app,
#     position='diagonal',
#     text='TESTING',
#     background='#9333ea',
#     color='#ffffff',
#     opacity=0.6
# )

# 8. No banner - comment out ALL envbanner.flask(...) lines above
#    IMPORTANT: You must restart the server (Ctrl+C, then run python test/flask-app.py again)

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
  <title>env-banner Test</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      max-width: 800px;
      margin: 50px auto;
      padding: 20px;
    }
    h1 { color: #1e40af; }
    .test-content {
      background: #f3f4f6;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
    }
    code {
      background: #e5e7eb;
      padding: 2px 6px;
      border-radius: 4px;
    }
  </style>
</head>
<body>
  <h1>env-banner (Python) Test Page</h1>
  <div class="test-content">
    <h2>Banner Configuration</h2>
    <p>You should see an environment banner on this page.</p>
    <p>Edit <code>test/flask-app.py</code> to test different configurations.</p>

    <h3>Available Positions:</h3>
    <ul>
      <li><strong>No position specified</strong> - Bottom bar <strong>(DEFAULT)</strong></li>
      <li><code>bottom</code> - Bottom bar (same as default)</li>
      <li><code>top</code> - Top bar</li>
      <li><code>diagonal</code> or <code>diagonal-bltr</code> - Diagonal stripe bottom-left to top-right (/)</li>
      <li><code>diagonal-tlbr</code> - Diagonal stripe top-left to bottom-right (\\)</li>
      <li><code>top-right</code> - Top-right corner ribbon</li>
      <li><code>top-left</code> - Top-left corner ribbon</li>
      <li><code>bottom-right</code> - Bottom-right corner ribbon</li>
      <li><code>bottom-left</code> - Bottom-left corner ribbon</li>
    </ul>

    <p><strong>Note:</strong> After changing the configuration in <code>test/flask-app.py</code>, you must restart the Flask server (Ctrl+C, then run <code>python test/flask-app.py</code> again).</p>

    <h3>Custom Options:</h3>
    <ul>
      <li><code>text</code> - Custom banner text</li>
      <li><code>background</code> - Background color (hex)</li>
      <li><code>color</code> - Text color (hex)</li>
      <li><code>opacity</code> - Banner opacity (0.0 to 1.0)</li>
      <li><code>show_host</code> - Show hostname (default: True)</li>
    </ul>
  </div>
</body>
</html>
'''

if __name__ == '__main__':
    print(f'Test server running at http://localhost:{PORT}')
    print('Edit test/flask-app.py to test different banner configurations')
    app.run(port=PORT, debug=True)
