# UniFi API OpenAPI Specifications

This repository contains OpenAPI 3.1.0 specifications for UniFi Network and Protect APIs, automatically extracted from UniFi controllers.

## ⚠️ Disclaimer

**This repository is not supported by Ubiquiti Inc.**

These OpenAPI specifications are extracted directly from the UniFi Network Application and UniFi Protect Application. While the specifications come from the official applications, this repository is community-maintained and not an official Ubiquiti project.

## Available Versions

### UniFi Network API

1 version(s) available:

- [10.1.68](unifi-network/10.1.68.json)


### UniFi Protect API

1 version(s) available:

- [6.2.72](unifi-protect/6.2.72.json)


## Directory Structure

```
unifi-network/
  ├── 10.1.68.json
  └── ...
unifi-protect/
  ├── 6.2.72.json
  └── ...
```

## Documentation

Interactive HTML documentation is automatically generated from the OpenAPI specifications and published via GitHub Pages.

**View the documentation at: [beez.ly/unifi-apis](https://beez.ly/unifi-apis)**

### Building Documentation Locally

To build the documentation locally:

```bash
python3 build_docs.py
```

This will generate HTML documentation in the `docs/` directory using ReDoc.

### Automatic Documentation Updates

Documentation is automatically rebuilt and deployed when:
- New OpenAPI spec files are added to `unifi-network/` or `unifi-protect/`
- The `build_docs.py` script is updated
- Changes are pushed to the main branch

The GitHub Actions workflow handles building and deploying the documentation to GitHub Pages automatically.

## Usage

These OpenAPI specifications can be used to:
- Generate API clients in various languages
- Generate API documentation
- Validate API requests and responses
- Understand API capabilities and changes between versions

## Generating Python Clients

```bash
# Install openapi-python-client
pip install openapi-python-client

# Generate Network API client
openapi-python-client generate --path unifi-network/10.1.68.json --output-path unifi-network-client

# Generate Protect API client
openapi-python-client generate --path unifi-protect/6.2.72.json --output-path unifi-protect-client
```

## Notes

- These specifications are automatically extracted from UniFi controllers
- Specifications are in OpenAPI 3.1.0 format
- Each version is stored as a separate file for easy comparison and version management
- Updates are published automatically when new versions are detected

## Setting Up GitHub Pages

To enable the documentation website:

1. Go to your repository on GitHub
2. Navigate to Settings > Pages
3. Under "Build and deployment", select:
   - Source: GitHub Actions
4. The workflow will automatically deploy on the next push to main

Your documentation will be available at your GitHub Pages URL within a few minutes.

## Last Updated

2025-12-25
