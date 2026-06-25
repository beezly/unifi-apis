# UniFi API OpenAPI Specifications

This repository contains OpenAPI 3.1.0 specifications for UniFi Network and Protect APIs, automatically extracted from UniFi controllers.

## Available Versions

### UniFi Network API

29 version(s) available:

- [10.5.51](unifi-network/10.5.51.json)
- [10.5.43](unifi-network/10.5.43.json)
- [10.4.57](unifi-network/10.4.57.json)
- [10.4.55](unifi-network/10.4.55.json)
- [10.4.46](unifi-network/10.4.46.json)
- [10.3.58](unifi-network/10.3.58.json)
- [10.3.55](unifi-network/10.3.55.json)
- [10.3.52](unifi-network/10.3.52.json)
- [10.3.47](unifi-network/10.3.47.json)
- [10.2.105](unifi-network/10.2.105.json)
- [10.2.104](unifi-network/10.2.104.json)
- [10.2.97](unifi-network/10.2.97.json)
- [10.2.93](unifi-network/10.2.93.json)
- [10.2.84](unifi-network/10.2.84.json)
- [10.2.78](unifi-network/10.2.78.json)
- [10.1.89](unifi-network/10.1.89.json)
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

33 version(s) available:

- [7.1.83](unifi-protect/7.1.83.json)
- [7.1.77](unifi-protect/7.1.77.json)
- [7.1.76](unifi-protect/7.1.76.json)
- [7.1.75](unifi-protect/7.1.75.json)
- [7.1.74](unifi-protect/7.1.74.json)
- [7.1.73](unifi-protect/7.1.73.json)
- [7.1.69](unifi-protect/7.1.69.json)
- [7.1.60](unifi-protect/7.1.60.json)
- [7.1.55](unifi-protect/7.1.55.json)
- [7.1.47](unifi-protect/7.1.47.json)
- [7.1.46](unifi-protect/7.1.46.json)
- [7.1.42](unifi-protect/7.1.42.json)
- [7.0.107](unifi-protect/7.0.107.json)
- [7.0.106](unifi-protect/7.0.106.json)
- [7.0.104](unifi-protect/7.0.104.json)
- [7.0.94](unifi-protect/7.0.94.json)
- [7.0.88](unifi-protect/7.0.88.json)
- [7.0.85](unifi-protect/7.0.85.json)
- [7.0.83](unifi-protect/7.0.83.json)
- [7.0.73](unifi-protect/7.0.73.json)
- [7.0.70](unifi-protect/7.0.70.json)
- [7.0.66](unifi-protect/7.0.66.json)
- [7.0.64](unifi-protect/7.0.64.json)
- [7.0.59](unifi-protect/7.0.59.json)
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
  ├── 10.5.51.json
  └── ...
unifi-protect/
  ├── 7.1.83.json
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
openapi-python-client generate --path unifi-network/10.5.51.json --output-path unifi-network-client

# Generate Protect API client
openapi-python-client generate --path unifi-protect/7.1.83.json --output-path unifi-protect-client
```

## Notes

- These specifications are automatically extracted from UniFi controllers
- Specifications are in OpenAPI 3.1.0 format
- Each version is stored as a separate file for easy comparison and version management
- Updates are published automatically when new versions are detected
