# Test Files

This directory contains test files for the `env-banner` Python package. **These files are NOT published to PyPI** (excluded in `pyproject.toml`).

## Flask Test Server

Run the Flask test server to see the banner in action:

```bash
# Install Flask if you don't have it
pip install flask

# Run the test server from the project root
python test/flask-app.py
```

Then visit `http://localhost:5000` in your browser.

Edit `test/flask-app.py` to test different banner configurations. After making changes, restart the server (Ctrl+C, then run again).

## Standalone HTML Test Files

Open these HTML files directly in your browser to test each banner position:

### Bar Positions
- **`test-top.html`** - Top bar
- **`test-bottom.html`** - Bottom bar (DEFAULT)

### Corner Ribbons
- **`test-top-left.html`** - Top-left corner ribbon
- **`test-top-right.html`** - Top-right corner ribbon
- **`test-bottom-left.html`** - Bottom-left corner ribbon
- **`test-bottom-right.html`** - Bottom-right corner ribbon

### Diagonal Stripes
- **`test-diagonal-tlbr.html`** - Diagonal stripe from top-left to bottom-right (\)
- **`test-diagonal-bltr.html`** - Diagonal stripe from bottom-left to top-right (/) - DEFAULT diagonal

## Testing Workflow

1. **Start with standalone HTML files** - Quick visual verification of each position
2. **Use Flask test server** - Test middleware integration and custom options
3. **Test in your own app** - Integrate into your actual application

## Position Options Summary

| Position | Description | Default Opacity |
|----------|-------------|-----------------|
| `bottom` | Full-width bar at bottom | 1.0 |
| `top` | Full-width bar at top | 1.0 |
| `top-left` | Corner ribbon (top-left) | 1.0 |
| `top-right` | Corner ribbon (top-right) | 1.0 |
| `bottom-left` | Corner ribbon (bottom-left) | 1.0 |
| `bottom-right` | Corner ribbon (bottom-right) | 1.0 |
| `diagonal` or `diagonal-bltr` | Diagonal stripe (/) | 0.5 |
| `diagonal-tlbr` | Diagonal stripe (\) | 0.5 |

## Custom Options

All positions support these custom options:
- `text` - Custom banner text
- `background` - Background color (hex)
- `color` - Text color (hex)
- `opacity` - Banner opacity (0.0 to 1.0)
- `show_host` - Whether to display hostname (default: True)
