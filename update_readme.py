#!/usr/bin/env python3
"""
Update README.md with current API versions in reverse order (most recent first).
"""

from pathlib import Path
from packaging import version


def get_spec_files(directory):
    """Get all JSON spec files from a directory, sorted in reverse version order."""
    path = Path(directory)
    if not path.exists():
        return []

    # Sort by semantic version in reverse order (most recent first)
    files = list(path.glob("*.json"))
    return sorted(files, key=lambda f: version.parse(f.stem), reverse=True)


def update_readme():
    """Update README.md with current API versions."""

    # Get all spec files
    network_specs = get_spec_files("unifi-network")
    protect_specs = get_spec_files("unifi-protect")

    # Build version lists (already in reverse order from get_spec_files)
    network_versions = "\n".join([f"- [{spec.stem}](unifi-network/{spec.name})" for spec in network_specs])
    protect_versions = "\n".join([f"- [{spec.stem}](unifi-protect/{spec.name})" for spec in protect_specs])

    readme_content = f"""# UniFi API OpenAPI Specifications

This repository contains OpenAPI 3.1.0 specifications for UniFi Network and Protect APIs, automatically extracted from UniFi controllers.

## Available Versions

### UniFi Network API

{len(network_specs)} version(s) available:

{network_versions if network_versions else "No versions available yet"}


### UniFi Protect API

{len(protect_specs)} version(s) available:

{protect_versions if protect_versions else "No versions available yet"}


## Directory Structure

```
unifi-network/
  ├── {network_specs[0].name if network_specs else "..."}
  └── ...
unifi-protect/
  ├── {protect_specs[0].name if protect_specs else "..."}
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
openapi-python-client generate --path unifi-network/{network_specs[0].name if network_specs else "VERSION.json"} --output-path unifi-network-client

# Generate Protect API client
openapi-python-client generate --path unifi-protect/{protect_specs[0].name if protect_specs else "VERSION.json"} --output-path unifi-protect-client
```

## Notes

- These specifications are automatically extracted from UniFi controllers
- Specifications are in OpenAPI 3.1.0 format
- Each version is stored as a separate file for easy comparison and version management
- Updates are published automatically when new versions are detected
"""

    # Write the updated README
    with open("README.md", "w") as f:
        f.write(readme_content)

    print("README.md updated successfully!")
    print(f"Network API versions: {len(network_specs)}")
    print(f"Protect API versions: {len(protect_specs)}")


if __name__ == "__main__":
    update_readme()
