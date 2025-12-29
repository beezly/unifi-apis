# Automated Version Request Validation

This document describes the proposed automation for validating and processing API version requests submitted via GitHub Issues.

## Overview

When users submit a new API version request using the issue template, an automated workflow will:

1. **Detect** if the issue is a valid version request for UniFi Protect or Network
2. **Validate** the version number format
3. **Check** if the version already exists in the repository
4. **Trigger** the spec generation workflow in the upstream repository

## Workflow Trigger

The automation triggers on new issues with the `api-request` label:

```yaml
on:
  issues:
    types: [opened, edited]
```

## Validation Steps

### 1. Issue Detection

The workflow parses the structured issue body to extract:
- **API Type**: UniFi Protect or UniFi Network
- **Version Number**: The requested version string

The issue template creates a predictable format with sections like:
```
### API Type
UniFi Protect

### Version Number
6.3.10
```

### 2. Version Format Validation

The version number must match the semantic version pattern:

```regex
^[0-9]+\.[0-9]+\.[0-9]+$
```

**Valid examples:** `6.3.10`, `10.1.68`, `5.3.48`
**Invalid examples:** `v6.3.10`, `6.3`, `6.3.10-beta`, `6.3.10.1`

### 3. Duplicate Check

The workflow checks if the version already exists by looking for:
- `unifi-protect/{version}.json` for Protect requests
- `unifi-network/{version}.json` for Network requests

### 4. Validation Response

| Outcome | Action |
|---------|--------|
| Valid & New | Add `validated` label, trigger spec generation |
| Invalid Format | Add `invalid` label, comment explaining the issue |
| Already Exists | Add `duplicate` label, comment with link to existing spec |

## External Workflow Trigger

For valid requests, the workflow triggers the `fetch-protect-specs` or `fetch-network-specs` workflow in the `beezly/unifi-openapi-specs-generator` repository:

```yaml
- uses: actions/github-script@v7
  with:
    github-token: ${{ secrets.SPEC_GENERATOR_PAT }}
    script: |
      await github.rest.actions.createWorkflowDispatch({
        owner: 'beezly',
        repo: 'unifi-openapi-specs-generator',
        workflow_id: 'fetch-protect-specs.yml',
        ref: 'main',
        inputs: {
          version: '${{ env.VERSION }}'
        }
      });
```

## Required Setup

### Secrets

| Secret | Description |
|--------|-------------|
| `SPEC_GENERATOR_PAT` | Personal Access Token with `workflow` scope to trigger workflows in `unifi-openapi-specs-generator` |

### Labels

The following labels should exist in the repository:

| Label | Description |
|-------|-------------|
| `api-request` | Applied by issue template (already exists) |
| `validated` | Version request passed validation |
| `invalid` | Version format is invalid |
| `duplicate` | Version already exists in repository |
| `protect` | Request is for UniFi Protect API |
| `network` | Request is for UniFi Network API |

## Workflow Diagram

```
┌─────────────────────┐
│   Issue Created     │
│  (api-request label)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Parse Issue Body   │
│  Extract API Type   │
│  Extract Version    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐     ┌─────────────────────┐
│ Version Format OK?  │─No─▶│  Add 'invalid' label│
│ (regex validation)  │     │  Comment on issue   │
└──────────┬──────────┘     └─────────────────────┘
           │Yes
           ▼
┌─────────────────────┐     ┌─────────────────────┐
│  Version Exists?    │─Yes▶│ Add 'duplicate' label│
│  (check for file)   │     │  Comment on issue   │
└──────────┬──────────┘     └─────────────────────┘
           │No
           ▼
┌─────────────────────┐
│  Add 'validated'    │
│  Add API type label │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Trigger Spec Gen    │
│ Workflow (external) │
└─────────────────────┘
```

## Future Enhancements

- **Auto-close issues** when spec is successfully generated and merged
- **Progress comments** showing spec generation status
- **Release channel handling** to filter EA/RC versions if needed
