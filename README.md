# UniFi API OpenAPI Specifications

This repository contains OpenAPI 3.1.0 specifications for UniFi Network and Protect APIs, automatically extracted from UniFi controllers.

## Available Versions

### UniFi Network API

13 version(s) available:

- [10.1.85](unifi-network/10.1.85.json)
- [10.1.84](unifi-network/10.1.84.json)
- [10.1.83](unifi-network/10.1.83.json)
- [10.1.80](unifi-network/10.1.80.json)
- [10.1.78](unifi-network/10.1.78.json)
- [10.1.68](unifi-network/10.1.68.json)
- [10.0.162](unifi-network/10.0.162.json)
- [9.5.21](unifi-network/9.5.21.json)
- [9.4.19](unifi-network/9.4.19.json)
- [9.3.45](unifi-network/9.3.45.json)
- [9.2.87](unifi-network/9.2.87.json)
- [9.1.120](unifi-network/9.1.120.json)
- [9.0.99](unifi-network/9.0.99.json)


### UniFi Protect API

9 version(s) available:

- [6.2.88](unifi-protect/6.2.88.json)
- [6.2.87](unifi-protect/6.2.87.json)
- [6.2.83](unifi-protect/6.2.83.json)
- [6.2.79](unifi-protect/6.2.79.json)
- [6.2.77](unifi-protect/6.2.77.json)
- [6.2.72](unifi-protect/6.2.72.json)
- [6.1.79](unifi-protect/6.1.79.json)
- [6.0.53](unifi-protect/6.0.53.json)
- [5.3.48](unifi-protect/5.3.48.json)


## Directory Structure

```
unifi-network/
  ├── 10.1.85.json
  └── ...
unifi-protect/
  ├── 6.2.88.json
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
openapi-python-client generate --path unifi-network/10.1.85.json --output-path unifi-network-client

# Generate Protect API client
openapi-python-client generate --path unifi-protect/6.2.88.json --output-path unifi-protect-client
```

## Notes

- These specifications are automatically extracted from UniFi controllers
- Specifications are in OpenAPI 3.1.0 format
- Each version is stored as a separate file for easy comparison and version management
- Updates are published automatically when new versions are detected
