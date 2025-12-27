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

    network_items = ""
    for spec in network_specs:
        version = spec_to_version(spec)
        network_items += f"""                <div class="version-card">
                    <div class="version-info">
                        <div class="version-number">Version {version}</div>
                    </div>
                    <div class="links">
                        <a href="network-{version}.html" class="btn btn-primary">View Documentation</a>
                        <a href="network-{version}.json" class="btn btn-secondary">Download Spec</a>
                    </div>
                </div>
"""

    protect_items = ""
    for spec in protect_specs:
        version = spec_to_version(spec)
        protect_items += f"""                <div class="version-card">
                    <div class="version-info">
                        <div class="version-number">Version {version}</div>
                    </div>
                    <div class="links">
                        <a href="protect-{version}.html" class="btn btn-primary">View Documentation</a>
                        <a href="protect-{version}.json" class="btn btn-secondary">Download Spec</a>
                    </div>
                </div>
"""

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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 2rem;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 3rem;
        }}

        header {{
            text-align: center;
            margin-bottom: 3rem;
            padding-bottom: 2rem;
            border-bottom: 2px solid #e0e0e0;
        }}

        h1 {{
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }}

        .subtitle {{
            color: #7f8c8d;
            font-size: 1.1rem;
        }}

        .disclaimer {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            margin: 2rem 0;
            border-radius: 4px;
        }}

        .disclaimer strong {{
            color: #856404;
        }}

        .api-section {{
            margin: 2rem 0;
        }}

        .api-section h2 {{
            color: #34495e;
            font-size: 1.8rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
        }}

        .api-section h2::before {{
            content: '';
            display: inline-block;
            width: 4px;
            height: 1.5rem;
            background: #667eea;
            margin-right: 0.75rem;
            border-radius: 2px;
        }}

        .version-list {{
            display: grid;
            gap: 1rem;
            margin-top: 1rem;
        }}

        .version-card {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.25rem;
            background: #f8f9fa;
            border-radius: 8px;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}

        .version-card:hover {{
            background: #e9ecef;
            border-color: #667eea;
            transform: translateX(4px);
        }}

        .version-info {{
            flex: 1;
        }}

        .version-number {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #2c3e50;
        }}

        .links {{
            display: flex;
            gap: 1rem;
        }}

        .btn {{
            padding: 0.6rem 1.5rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            display: inline-block;
        }}

        .btn-primary {{
            background: #667eea;
            color: white;
        }}

        .btn-primary:hover {{
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }}

        .btn-secondary {{
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }}

        .btn-secondary:hover {{
            background: #667eea;
            color: white;
        }}

        footer {{
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 2px solid #e0e0e0;
            text-align: center;
            color: #7f8c8d;
        }}

        footer a {{
            color: #667eea;
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        .empty-state {{
            text-align: center;
            padding: 2rem;
            color: #7f8c8d;
            font-style: italic;
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
            <strong>⚠️ Disclaimer:</strong> This repository is not supported by Ubiquiti Inc. These OpenAPI specifications are extracted directly from the UniFi applications and are community-maintained.
        </div>

        <section class="api-section">
            <h2>UniFi Network API</h2>
            <div class="version-list">
{network_items if network_items else '                <div class="empty-state">No versions available yet</div>'}
            </div>
        </section>

        <section class="api-section">
            <h2>UniFi Protect API</h2>
            <div class="version-list">
{protect_items if protect_items else '                <div class="empty-state">No versions available yet</div>'}
            </div>
        </section>

        <footer>
            <p>Last Updated: {date.today().strftime('%Y-%m-%d')}</p>
            <p>Generated automatically from OpenAPI specifications</p>
            <p><a href="https://github.com/beezly/unifi-apis">View on GitHub</a></p>
        </footer>
    </div>
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
