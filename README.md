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

## Last Updated

2025-12-25
