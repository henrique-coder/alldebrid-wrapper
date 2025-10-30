<div align="center">

# ⚙️ AllDebrid Wrapper

A modern, fully-typed Python wrapper for the [AllDebrid API](https://docs.alldebrid.com).

[![Version](https://img.shields.io/badge/dynamic/toml?url=https://raw.githubusercontent.com/henrique-coder/alldebrid-wrapper/main/pyproject.toml&query=$.project.version&label=Version&color=orange)](./pyproject.toml)
[![Python](https://img.shields.io/badge/dynamic/toml?url=https://raw.githubusercontent.com/henrique-coder/alldebrid-wrapper/main/pyproject.toml&query=$.project.requires-python&label=Python&color=blue)](https://www.python.org/downloads)
[![License](https://img.shields.io/github/license/henrique-coder/alldebrid-wrapper?color=green)](./LICENSE)

</div>

## Features

- 🔒 **Type-safe** - Full type hints and Pydantic models
- 📦 **Complete** - All API endpoints implemented
- 🎯 **Easy to use** - Intuitive interface with helpful docstrings
- ⚡ **Fast** - Uses orjson for high-performance JSON parsing
- 🛡️ **Robust** - Comprehensive error handling

## Installation

```bash
uv add git+https://github.com/henrique-coder/alldebrid-wrapper.git --branch main
```

## Quick Start

### Basic Usage

```python
from alldebrid_wrapper import AllDebridAPI

# Initialize with API key
client = AllDebridAPI(api_key="your_api_key_here")

# Get user information
user_info = client.get_user()
print(user_info.data)

# Unlock a URL
result = client.unlock_url("https://example.com/file")
print(result.data)
```

### Using Context Manager (Recommended)

```python
from alldebrid_wrapper import AllDebridAPI

with AllDebridAPI(api_key="your_api_key") as client:
    # Get supported hosts
    hosts = client.get_supported_hosts()
    print(hosts.data)

    # Upload magnets
    magnets = client.upload_magnet_uris([
        "magnet:?xt=urn:btih:..."
    ])
    print(magnets.data)
```

### Public Endpoints (No API Key Required)

```python
from alldebrid_wrapper import AllDebridAPI

# Initialize without API key for public endpoints
client = AllDebridAPI()

# Check API status
ping = client.ping()
print(ping.data)  # {'status': 'success', 'data': {'ping': 'pong', ...}}

# Get supported hosts
hosts = client.get_supported_hosts()
print(hosts.data)
```

### Dynamic API Key Management

```python
from alldebrid_wrapper import AllDebridAPI

client = AllDebridAPI()

# Use public endpoints
client.ping()

# Set API key for private endpoints
client.set_api_key("your_api_key")
user = client.get_user()

# Remove API key
client.remove_api_key()

# Back to public endpoints only
client.ping()
```

## API Coverage

### Public Endpoints

- ✅ `ping()` - Check API availability
- ✅ `get_supported_hosts()` - Get all supported hosts
- ✅ `get_supported_domains()` - Get supported domains
- ✅ `get_host_priorities()` - Get host priority rankings

### User Endpoints

- ✅ `get_user()` - Get user account info
- ✅ `get_user_supported_hosts()` - Get user-specific host quotas
- ✅ `get_saved_urls()` - Get saved URLs
- ✅ `save_urls()` - Save URLs for later
- ✅ `delete_saved_urls()` - Delete saved URLs
- ✅ `get_recent_urls()` - Get recent download history
- ✅ `delete_recent_urls()` - Clear recent history

### Link/URL Endpoints

- ✅ `get_url_info()` - Get URL info without unlocking
- ✅ `extract_redirector_urls()` - Extract real URLs from shorteners
- ✅ `unlock_url()` - Unlock premium URLs
- ✅ `select_stream_quality()` - Select video stream quality
- ✅ `check_delayed_url()` - Check delayed unlock status

### Magnet/Torrent Endpoints

- ✅ `upload_magnet_uris()` - Upload magnet links
- ✅ `upload_torrent_files()` - Upload .torrent files
- ✅ `get_magnet_status()` - Get single magnet status
- ✅ `get_all_magnets_status()` - Get all magnets with filtering
- ✅ `get_all_magnets_incremental()` - Delta sync for magnets
- ✅ `get_magnet_files()` - Get files from magnets
- ✅ `delete_magnet()` - Delete a magnet
- ✅ `restart_magnet()` - Restart failed magnet
- ✅ `restart_magnets()` - Restart multiple magnets

### PIN Authentication (Resellers)

- ✅ `get_pin_code()` - Generate PIN for authentication
- ✅ `check_pin_status()` - Check PIN authentication status

### Reseller Endpoints

- ✅ `get_reseller_balance()` - Get reseller balance
- ✅ `get_reseller_vouchers()` - Get existing vouchers
- ✅ `generate_reseller_vouchers()` - Generate new vouchers

## Error Handling

```python
from alldebrid_wrapper import (
    AllDebridAPI,
    AllDebridAPIError,
    AllDebridHTTPError,
    AllDebridMissingAPIKeyError,
)

client = AllDebridAPI()

try:
    # This will fail - no API key
    user = client.get_user()
except AllDebridMissingAPIKeyError as e:
    print(f"API key required: {e.message}")

try:
    # This will fail - invalid URL
    result = client.unlock_url("invalid_url")
except AllDebridAPIError as e:
    print(f"API error: {e.message}")
    print(f"Status code: {e.response.status_code}")
```

## Advanced Usage

### Magnet Status Filtering

```python
with AllDebridAPI(api_key="your_key") as client:
    # Get all magnets
    all_magnets = client.get_all_magnets_status()

    # Get only ready magnets
    ready = client.get_all_magnets_status(status=["ready"])

    # Get processing magnets
    processing = client.get_all_magnets_status(status=["processing"])

    # Get error magnets
    errors = client.get_all_magnets_status(status=["error"])

    # Combine filters
    active = client.get_all_magnets_status(
        status=["downloading", "uploading", "compressing"]
    )
```

### Incremental Magnet Sync

```python
with AllDebridAPI(api_key="your_key") as client:
    session_id = 1  # Your app ID
    counter = 0     # Start from 0

    while True:
        # Get only changes since last call
        response = client.get_all_magnets_incremental(
            session_id=session_id,
            counter=counter
        )

        # Update counter for next call
        counter = response.data["data"]["counter"]

        # Process new/changed magnets
        magnets = response.data["data"]["magnets"]
        for magnet in magnets:
            print(f"Magnet {magnet['id']}: {magnet['status']}")

        time.sleep(5)  # Poll every 5 seconds
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [AllDebrid API Documentation](https://docs.alldebrid.com)
- [GitHub Repository](https://github.com/henrique-coder/alldebrid-wrapper)

## Disclaimer

This is an unofficial wrapper for the AllDebrid API. Not affiliated with or endorsed by AllDebrid.
