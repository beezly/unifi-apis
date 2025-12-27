#!/usr/bin/env python3
"""
Build script to generate HTML documentation from OpenAPI specs.
Automatically discovers all spec files and generates ReDoc documentation.
"""

import os
import json
import shutil
from pathlib import Path
from datetime import date
from packaging import version


def get_spec_files(directory):
    """Get all JSON spec files from a directory, sorted in reverse version order."""
    path = Path(directory)
    if not path.exists():
        return []

    # Sort by semantic version in reverse order (most recent first)
    files = list(path.glob("*.json"))
    return sorted(files, key=lambda f: version.parse(f.stem), reverse=True)


def generate_redoc_html(spec_filename, output_path, title):
    """Generate a standalone ReDoc HTML page for a spec."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
        }}
    </style>
</head>
<body>
    <redoc spec-url="{spec_filename}"></redoc>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"></script>
</body>
</html>
"""

    with open(output_path, 'w') as f:
        f.write(html)


def generate_index_html(network_specs, protect_specs, output_path):
    """Generate the main index.html landing page."""

    def spec_to_version(spec_file):
        return spec_file.stem

    def generate_version_rows(specs, api_type):
        """Generate version row HTML for older versions (skip first/latest)."""
        rows = ""
        for spec in specs[1:]:  # Skip the latest version
            ver = spec_to_version(spec)
            rows += f"""                        <div class="version-row">
                            <span class="version-num">{ver}</span>
                            <div class="version-links">
                                <a href="{api_type}-{ver}.html" class="btn btn-secondary btn-xs">Docs</a>
                                <a href="{api_type}-{ver}.json" class="btn btn-secondary btn-xs">JSON</a>
                            </div>
                        </div>
"""
        return rows

    # Get latest versions
    network_latest = spec_to_version(network_specs[0]) if network_specs else None
    protect_latest = spec_to_version(protect_specs[0]) if protect_specs else None

    # Generate older version rows
    network_older = generate_version_rows(network_specs, "network")
    protect_older = generate_version_rows(protect_specs, "protect")

    # Older versions toggle (only if there are older versions)
    network_toggle = ""
    if len(network_specs) > 1:
        network_toggle = f"""                    <button class="versions-toggle" onclick="toggleVersions(this)">
                        <span>Older versions</span>
                        <svg viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
                    </button>
                    <div class="versions-list">
{network_older}                    </div>"""

    protect_toggle = ""
    if len(protect_specs) > 1:
        protect_toggle = f"""                    <button class="versions-toggle" onclick="toggleVersions(this)">
                        <span>Older versions</span>
                        <svg viewBox="0 0 24 24"><path d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"/></svg>
                    </button>
                    <div class="versions-list">
{protect_older}                    </div>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UniFi API Documentation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #1a1a2e;
            min-height: 100vh;
            padding: 2rem;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
        }}

        header {{
            text-align: center;
            margin-bottom: 2rem;
            color: white;
        }}

        h1 {{
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            color: rgba(255,255,255,0.7);
            font-size: 1rem;
        }}

        .disclaimer {{
            background: rgba(255, 193, 7, 0.15);
            border: 1px solid rgba(255, 193, 7, 0.3);
            color: #ffc107;
            padding: 0.75rem 1rem;
            margin-bottom: 2rem;
            border-radius: 8px;
            font-size: 0.9rem;
            text-align: center;
        }}

        .api-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        @media (max-width: 800px) {{
            .api-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .api-card {{
            background: #16213e;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .api-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.4);
        }}

        .card-header {{
            padding: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .card-header.network {{
            background: linear-gradient(135deg, #0f4c75 0%, #1a237e 100%);
        }}

        .card-header.protect {{
            background: linear-gradient(135deg, #5c2a7e 0%, #7b1fa2 100%);
        }}

        .card-icon {{
            width: 48px;
            height: 48px;
            background: rgba(255,255,255,0.15);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .card-icon svg {{
            width: 24px;
            height: 24px;
            fill: white;
        }}

        .card-title {{
            flex: 1;
        }}

        .card-title h2 {{
            color: white;
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 0.15rem;
        }}

        .card-title .version-count {{
            color: rgba(255,255,255,0.7);
            font-size: 0.85rem;
        }}

        .card-body {{
            padding: 1.5rem;
        }}

        .latest-section {{
            margin-bottom: 1rem;
        }}

        .latest-label {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #888;
            margin-bottom: 0.5rem;
        }}

        .latest-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1rem;
        }}

        .latest-version {{
            font-size: 1.5rem;
            font-weight: 700;
            color: white;
        }}

        .btn-group {{
            display: flex;
            gap: 0.5rem;
        }}

        .btn {{
            padding: 0.5rem 1rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            border: none;
            cursor: pointer;
        }}

        .btn svg {{
            width: 14px;
            height: 14px;
        }}

        .btn-primary {{
            background: #3b82f6;
            color: white;
        }}

        .btn-primary:hover {{
            background: #2563eb;
        }}

        .btn-secondary {{
            background: rgba(255,255,255,0.1);
            color: #ccc;
        }}

        .btn-secondary:hover {{
            background: rgba(255,255,255,0.15);
            color: white;
        }}

        .versions-toggle {{
            width: 100%;
            padding: 0.75rem 1rem;
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            color: #999;
            font-size: 0.9rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.2s ease;
        }}

        .versions-toggle:hover {{
            background: rgba(255,255,255,0.08);
            border-color: rgba(255,255,255,0.2);
            color: #ccc;
        }}

        .versions-toggle svg {{
            width: 16px;
            height: 16px;
            fill: currentColor;
            transition: transform 0.2s ease;
        }}

        .versions-toggle.open svg {{
            transform: rotate(180deg);
        }}

        .versions-list {{
            display: none;
            margin-top: 0.75rem;
        }}

        .versions-list.open {{
            display: block;
        }}

        .version-row {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.6rem 0.75rem;
            background: rgba(255,255,255,0.03);
            border-radius: 6px;
            margin-bottom: 0.4rem;
            transition: background 0.2s ease;
        }}

        .version-row:hover {{
            background: rgba(255,255,255,0.08);
        }}

        .version-row:last-child {{
            margin-bottom: 0;
        }}

        .version-num {{
            color: #ddd;
            font-weight: 500;
            font-size: 0.9rem;
            font-family: 'SF Mono', 'Fira Code', 'Consolas', monospace;
        }}

        .version-links {{
            display: flex;
            gap: 0.5rem;
        }}

        .btn-xs {{
            padding: 0.3rem 0.6rem;
            font-size: 0.75rem;
        }}

        footer {{
            text-align: center;
            color: rgba(255,255,255,0.4);
            font-size: 0.85rem;
            padding-top: 1rem;
        }}

        footer a {{
            color: rgba(255,255,255,0.6);
            text-decoration: none;
        }}

        footer a:hover {{
            color: white;
            text-decoration: underline;
        }}

        footer p {{
            margin-bottom: 0.3rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>UniFi API Documentation</h1>
            <p class="subtitle">OpenAPI 3.1.0 Specifications for UniFi Network and Protect APIs</p>
        </header>

        <div class="disclaimer">
            <strong>Disclaimer:</strong> Not supported by Ubiquiti Inc. Community-maintained specifications extracted from UniFi applications.
        </div>

        <div class="api-grid">
            <!-- Network API Card -->
            <div class="api-card">
                <div class="card-header network">
                    <div class="card-icon">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                        </svg>
                    </div>
                    <div class="card-title">
                        <h2>Network API</h2>
                        <span class="version-count">{len(network_specs)} version{"s" if len(network_specs) != 1 else ""} available</span>
                    </div>
                </div>
                <div class="card-body">
                    <div class="latest-section">
                        <div class="latest-label">Latest Version</div>
                        <div class="latest-row">
                            <span class="latest-version">{network_latest or "N/A"}</span>
                            <div class="btn-group">
                                <a href="network-{network_latest}.html" class="btn btn-primary">
                                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm-1 7V3.5L18.5 9H13z"/></svg>
                                    Docs
                                </a>
                                <a href="network-{network_latest}.json" class="btn btn-secondary">
                                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
                                    JSON
                                </a>
                            </div>
                        </div>
                    </div>
{network_toggle}
                </div>
            </div>

            <!-- Protect API Card -->
            <div class="api-card">
                <div class="card-header protect">
                    <div class="card-icon">
                        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
                        </svg>
                    </div>
                    <div class="card-title">
                        <h2>Protect API</h2>
                        <span class="version-count">{len(protect_specs)} version{"s" if len(protect_specs) != 1 else ""} available</span>
                    </div>
                </div>
                <div class="card-body">
                    <div class="latest-section">
                        <div class="latest-label">Latest Version</div>
                        <div class="latest-row">
                            <span class="latest-version">{protect_latest or "N/A"}</span>
                            <div class="btn-group">
                                <a href="protect-{protect_latest}.html" class="btn btn-primary">
                                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zm-1 7V3.5L18.5 9H13z"/></svg>
                                    Docs
                                </a>
                                <a href="protect-{protect_latest}.json" class="btn btn-secondary">
                                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/></svg>
                                    JSON
                                </a>
                            </div>
                        </div>
                    </div>
{protect_toggle}
                </div>
            </div>
        </div>

        <footer>
            <p>Generated automatically from OpenAPI specifications</p>
            <p><a href="https://github.com/beezly/unifi-apis">View on GitHub</a></p>
        </footer>
    </div>

    <script>
        function toggleVersions(button) {{
            button.classList.toggle('open');
            const list = button.nextElementSibling;
            list.classList.toggle('open');
        }}
    </script>
</body>
</html>
"""

    with open(output_path, 'w') as f:
        f.write(html)


def main():
    """Main build function."""
    # Create docs directory if it doesn't exist
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    # Get all spec files
    network_specs = get_spec_files("unifi-network")
    protect_specs = get_spec_files("unifi-protect")

    print(f"Found {len(network_specs)} Network API spec(s)")
    print(f"Found {len(protect_specs)} Protect API spec(s)")

    # Copy JSON specs to docs directory and generate ReDoc pages
    for spec in network_specs:
        version = spec.stem
        # Copy JSON spec to docs
        dest_spec = docs_dir / f"network-{version}.json"
        shutil.copy2(spec, dest_spec)
        print(f"Copied: {dest_spec}")

        # Generate HTML page
        output_file = docs_dir / f"network-{version}.html"
        generate_redoc_html(
            f"network-{version}.json",
            output_file,
            f"UniFi Network API {version}"
        )
        print(f"Generated: {output_file}")

    for spec in protect_specs:
        version = spec.stem
        # Copy JSON spec to docs
        dest_spec = docs_dir / f"protect-{version}.json"
        shutil.copy2(spec, dest_spec)
        print(f"Copied: {dest_spec}")

        # Generate HTML page
        output_file = docs_dir / f"protect-{version}.html"
        generate_redoc_html(
            f"protect-{version}.json",
            output_file,
            f"UniFi Protect API {version}"
        )
        print(f"Generated: {output_file}")

    # Generate index page
    index_file = docs_dir / "index.html"
    generate_index_html(network_specs, protect_specs, index_file)
    print(f"Generated: {index_file}")

    print("\nDocumentation build complete!")
    print(f"Total pages generated: {len(network_specs) + len(protect_specs) + 1}")


if __name__ == "__main__":
    main()
