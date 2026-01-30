"""
Batch diagram generator using SyntaxTreeHybrid
Uses the tool's native exportPNG() for high-quality cropped images
"""

import os
import sys
import time
import base64
import threading
import http.server
import socketserver
from pathlib import Path

# Try to import playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("ERROR: Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Configuration
PORT = 8080
SYNTAX_TREE_DIR = Path(r"C:\Users\irphy\Documents\SyntaxTreeHybrid")
OUTPUT_DIR = Path(r"C:\Users\irphy\Documents\concise-guide-english-grammar\assets\diagrams\new")
BRACKET_FILE = OUTPUT_DIR / "bracket_notations.txt"

# Export resolution multiplier (higher = better quality, larger files)
# 3 = default, 5-6 = high quality for print/zoom
EXPORT_MULTIPLIER = 5

def log(msg):
    print(msg, flush=True)

def parse_bracket_file(filepath):
    """Parse the bracket notations file and return a dict of name -> bracket"""
    diagrams = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            # Parse "name | bracket" format
            if ' | ' in line:
                name, bracket = line.split(' | ', 1)
                diagrams[name.strip()] = bracket.strip()
    return diagrams

def start_server():
    """Start HTTP server for SyntaxTreeHybrid"""
    os.chdir(str(SYNTAX_TREE_DIR))
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *args: None  # Suppress logs
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

def save_data_url_as_png(data_url, filepath):
    """Convert a data URL to a PNG file"""
    # data:image/png;base64,XXXXX
    header, encoded = data_url.split(',', 1)
    data = base64.b64decode(encoded)
    with open(filepath, 'wb') as f:
        f.write(data)

def generate_diagrams(diagrams, start_from=None):
    """Generate PNG diagrams for all bracket notations"""
    log("=" * 70)
    log("SyntaxTreeHybrid - Batch Diagram Generation (High Quality)")
    log("=" * 70)
    log(f"Diagrams to generate: {len(diagrams)}")
    log(f"Output directory: {OUTPUT_DIR}")
    log(f"Export multiplier: {EXPORT_MULTIPLIER}x")
    log("")

    # Start server
    log("Starting HTTP server...")
    server = threading.Thread(target=start_server, daemon=True)
    server.start()
    time.sleep(1)

    results = []
    started = start_from is None

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 1400, "height": 900})

        for i, (name, bracket) in enumerate(diagrams.items()):
            # Skip until we reach start_from
            if not started:
                if name == start_from:
                    started = True
                else:
                    continue

            log(f"\n[{i+1:02d}/{len(diagrams)}] {name}")
            log("-" * 60)
            log(f"  Bracket: {bracket}")

            # Navigate to app
            page.goto(f"http://localhost:{PORT}/index.html")
            page.wait_for_selector("#diagram-canvas", state="visible")
            time.sleep(0.5)

            # Enter bracket notation
            bracket_input = page.locator("#bracket-input")
            bracket_input.click()
            bracket_input.fill(bracket)
            time.sleep(1.0)

            # Check status
            status = page.locator("#bracket-status").inner_text()
            success = "error" not in status.lower()

            # Retry if needed
            attempts = 1
            while not success and attempts < 3:
                log(f"  Attempt {attempts} failed ({status}), retrying...")
                attempts += 1
                bracket_input.fill("")
                time.sleep(0.3)
                bracket_input.fill(bracket)
                time.sleep(1.0)
                status = page.locator("#bracket-status").inner_text()
                success = "error" not in status.lower()

            if success:
                # Use the tool's native exportPNG() for high-quality cropped output
                try:
                    data_url = page.evaluate(f"""
                        async () => {{
                            // Wait a bit for rendering to complete
                            await new Promise(r => setTimeout(r, 200));
                            // Export at high resolution with tight crop
                            return await window.canvasManager.exportPNG({EXPORT_MULTIPLIER});
                        }}
                    """)

                    # Save the data URL as PNG
                    output_path = OUTPUT_DIR / f"{name}.png"
                    save_data_url_as_png(data_url, output_path)

                    log(f"  Status: {status}")
                    log(f"  Saved: {name}.png")
                    results.append({"name": name, "success": True, "status": status})
                except Exception as e:
                    log(f"  Export error: {e}")
                    results.append({"name": name, "success": False, "status": str(e)})
            else:
                log(f"  FAILED: {status}")
                results.append({"name": name, "success": False, "status": status})

            time.sleep(0.3)

        browser.close()

    # Summary
    log("\n" + "=" * 70)
    log("GENERATION SUMMARY")
    log("=" * 70)

    passed = sum(1 for r in results if r["success"])
    failed = len(results) - passed

    log(f"Successful: {passed}/{len(results)}")
    log(f"Failed: {failed}/{len(results)}")

    if failed > 0:
        log("\nFailed diagrams:")
        for r in results:
            if not r["success"]:
                log(f"  - {r['name']}: {r['status']}")

    log("\n" + "=" * 70)
    log("Generation complete!")
    log("=" * 70)

    return results

def main():
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Check for bracket file
    if not BRACKET_FILE.exists():
        log(f"ERROR: Bracket file not found: {BRACKET_FILE}")
        sys.exit(1)

    # Parse bracket notations
    log(f"Reading bracket notations from: {BRACKET_FILE}")
    diagrams = parse_bracket_file(BRACKET_FILE)
    log(f"Found {len(diagrams)} diagrams to generate")

    # Optional: start from a specific diagram (for resuming)
    start_from = None
    if len(sys.argv) > 1:
        start_from = sys.argv[1]
        log(f"Starting from: {start_from}")

    # Generate diagrams
    generate_diagrams(diagrams, start_from)

if __name__ == "__main__":
    main()
