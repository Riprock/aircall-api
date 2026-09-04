# Aircall API

A Python client library for the [Aircall.io](https://aircall.io) API, providing easy access to Aircall's telephony services.

Covers all 94 endpoints in the [Aircall API reference](https://developers.aircall.io/api-references), verified against the published documentation.

## Features

- Full type hints with Pydantic models
- Complete coverage of the documented Aircall REST API
- Basic Auth and OAuth 2.0 Bearer authentication
- Paginated results that expose Aircall's `meta` (total, current page, next page)
- Custom exceptions for proper error handling
- `DeprecationWarning` on endpoints Aircall is retiring, naming the replacement and date
- Comprehensive logging support for debugging and monitoring
- Python 3.13+ support

## Installation

```bash
pip install aircall-api
```

Or using `uv`:

```bash
uv add aircall-api
```

## Quick Start

```python
from aircall import AircallClient

client = AircallClient(api_id="your_api_id", api_token="your_api_token")

# List phone numbers
numbers = client.number.list_numbers()

# Get a specific number
number = client.number.get(12345)
```

## Authentication

Aircall supports two schemes. Use whichever matches your integration.

**Basic Auth** — for Aircall customers using their own account's API key:

1. Log in to your [Aircall Dashboard](https://dashboard.aircall.io)
2. Navigate to Settings > Integrations > API Keys
3. Create a new API key or use an existing one

```python
client = AircallClient(
    api_id="YOUR_API_ID",
    api_token="YOUR_API_TOKEN",
    timeout=30,      # Optional: request timeout in seconds
    verbose=False    # Optional: enable debug logging
)
```

**OAuth 2.0** — for technology partners acting on a customer's behalf:

```python
client = AircallClient(access_token="YOUR_OAUTH_ACCESS_TOKEN")

client.ping()  # {"ping": "pong"} -- verifies the token is accepted
```

Supplying neither scheme, or both, raises `ValueError`.

## Pagination

Every `list_*` method returns a `Page`. It behaves like a list, and additionally
carries the pagination metadata Aircall sends:

```python
page = client.call.list_calls(per_page=50)

for call in page:          # iterate like a list
    print(call.id)

page.meta.total            # total matching calls across all pages
page.meta.current_page
page.has_next              # whether another page exists
```

Walking every page:

```python
page_number = 1
while True:
    page = client.call.list_calls(page=page_number, per_page=50)
    for call in page:
        ...
    if not page.has_next:
        break
    page_number += 1
```

`per_page` is validated locally against the bounds Aircall enforces (1-50 for most
endpoints, 1-100 for SMS templates), so an out-of-range value raises `ValueError`
rather than spending a request on a 400.

## Available Resources

| Attribute | Resource | Notes |
|---|---|---|
| `client.call` | Calls | List, search, transfer, tag, recordings, Conversation Intelligence |
| `client.contact` | Contacts | Including phone numbers and emails |
| `client.number` | Numbers | Including registration status |
| `client.user` | Users (V1) | Deprecated by Aircall on 2026-09-30 |
| `client.userv2` | Users (V2) | The replacement; routed to `/v2` |
| `client.team` | Teams | |
| `client.tag` | Tags | |
| `client.message` | Messages | SMS, MMS, group, WhatsApp, templates |
| `client.webhook` | Webhooks | |
| `client.integration` | Integrations | |
| `client.dialer_campaign` | Dialer campaigns | |
| `client.company` | Company | |
| `client.ai_voice_agent` | AI Voice Agents | Trigger outbound agent calls |
| `client.analytics` | Analytics | Report exports; requires Analytics+ |

### Usage Examples

#### Working with Calls

```python
# List calls, newest first, with contact details included
page = client.call.list_calls(page=1, per_page=20, order="desc", fetch_contact=True)

# Get a specific call, including any AI Voice Agent segments
call = client.call.get(12345, fetch_aiva_conv=True)

# Search within a time range
page = client.call.search(**{"from": 1704067200, "to": 1706745600})

# Conversation Intelligence
client.call.get_transcription(12345, mode="realtime")
client.call.get_summary(12345)
client.call.get_predicted_csat(12345)
client.call.get_custom_summary_result(12345)
```

#### Working with Contacts

```python
page = client.contact.list_contacts()

contact = client.contact.create(
    first_name="John",
    last_name="Doe",
    phone_numbers=[{"label": "Work", "value": "+1234567890"}],
    emails=[{"label": "Office", "value": "john.doe@example.com"}],
)

client.contact.update(12345, emails=[{"label": "Personal", "value": "john@example.com"}])

page = client.contact.search(phone_number="+1234567890")
```

#### Working with Users

```python
# User V2 -- the current API
page = client.userv2.list_users()
user = client.userv2.get(456)
numbers = client.userv2.get_numbers(456)
```

#### Sending messages

Aircall splits sending into two channels, and the distinction matters:

```python
# Stored in the agent's Aircall inbox, visible to agents
client.message.send_in_conversation(number_id, to="+1234567890", body="Hello")

# Bypasses the inbox entirely, for automated or high-volume traffic.
# Register the number first with create_configuration().
client.message.send_skipping_inbox(number_id, to="+1234567890", body="Your code is 1234")

# Group and WhatsApp
client.message.send_group_in_conversation(number_id, ["+1555...", "+1556..."], "Hi all")
client.message.send_whatsapp_skipping_inbox(number_id, "+1234567890", text="Hello")

# Templates and channel health
client.message.list_sms_templates(search="order")
client.message.list_whatsapp_templates(number_id, status="APPROVED")
client.message.get_whatsapp_status(number_id)
```

#### AI Voice Agents and Analytics

```python
import time

request = client.ai_voice_agent.trigger_outbound_call(
    "agent-abc123",
    contact_phone="+15551234567",
    idempotency_key="appt-reminder-2026-03-15-cust-12345",
    context={"first_name": "Jane", "appointment_date": "March 20th at 2:00 PM"},
)

export = client.analytics.create_export(
    "CALLS_HISTORY",
    timezone="Europe/Paris",
    absolute_range={"fromDate": "2026-05-01", "toDate": "2026-05-15"},
    filters={"teamIDs": [4242]},
)
while client.analytics.get_export(export.exportID).is_pending:
    time.sleep(60)
```

## Deprecations

Aircall is retiring some endpoints. The SDK raises a `DeprecationWarning` naming
the replacement and the removal date rather than letting you find out from a 404.

| Deprecated | Replacement | Aircall removes |
|---|---|---|
| `client.user.list_users/get/create/update` | `client.userv2.*` | 2026-09-30 |
| `client.call.get_realtime_transcription()` | `client.call.get_transcription(id, mode="realtime")` | 2026-03-31 (passed) |
| `client.message.send()` | `client.message.send_skipping_inbox()` | — |
| `client.message.send_native()` | `client.message.send_in_conversation()` | — |

Surface them with:

```bash
python -W default::DeprecationWarning your_script.py
```

## Error Handling

The library provides custom exceptions for different error scenarios. All exceptions inherit from `AircallError`:

```python
from aircall import (
    AircallClient,
    ValidationError,
    AuthenticationError,
    NotFoundError,
    UnprocessableEntityError,
    RateLimitError,
    ServerError,
    AircallConnectionError,
    AircallTimeoutError,
)

client = AircallClient(api_id="your_id", api_token="your_token")

try:
    contact = client.contact.get(12345)
except NotFoundError:
    print("Contact not found")
except AuthenticationError:
    print("Invalid API credentials")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Invalid request: {e.message}")
except AircallTimeoutError:
    print("Request timed out")
except AircallConnectionError:
    print("Failed to connect to Aircall API")
```

### Available Exceptions

- **`ValidationError`** (400) - Invalid request payload or bad request
- **`AuthenticationError`** (401, 403) - Invalid API credentials
- **`NotFoundError`** (404) - Resource not found
- **`UnprocessableEntityError`** (422) - Server unable to process the request
- **`RateLimitError`** (429) - Rate limit exceeded (includes `retry_after` attribute)
- **`ServerError`** (5xx) - Aircall server error
- **`AircallConnectionError`** - Network connection failed
- **`AircallTimeoutError`** - Request timed out

All exceptions include:
- `message`: Error description
- `status_code`: HTTP status code (for API errors)
- `response_data`: Full error response from the API (if available)

## Logging

The Aircall SDK includes comprehensive logging capabilities to help you debug issues, monitor API requests, and track application behavior.

### Quick Start with Logging

Enable debug logging with the `verbose` parameter:

```python
from aircall import AircallClient

# Enable verbose logging (sets log level to DEBUG)
client = AircallClient(
    api_id="your_api_id",
    api_token="your_api_token",
    verbose=True  # Enables DEBUG level logging
)

# Now all API requests/responses will be logged
numbers = client.number.list_numbers()
```

### Configuring Logging Levels

For more control, configure logging manually using Python's standard `logging` module:

```python
import logging
from aircall import AircallClient, configure_logging

# Configure logging for the entire SDK
configure_logging(logging.INFO)

# Or configure logging for specific components
logging.getLogger('aircall.client').setLevel(logging.DEBUG)
logging.getLogger('aircall.resources').setLevel(logging.INFO)

client = AircallClient(api_id="your_id", api_token="your_token")
```

### Log Levels and What They Capture

- **DEBUG**: Detailed request/response information
  - Request method, URL, query parameters, request body
  - Response status codes and timing
  - Example: `Request: GET https://api.aircall.io/v1/numbers?page=1`

- **INFO**: High-level operation information
  - Client initialization
  - Critical operations (call transfers, deletions)
  - Example: `Aircall client initialized`

- **WARNING**: Important events that may need attention
  - API errors and HTTP error status codes
  - Rate limit warnings
  - Destructive operations (deleting recordings/voicemails)
  - Example: `API error: 404 GET /calls/999 - Not Found (took 0.34s)`

- **ERROR**: Failures and exceptions
  - Connection errors
  - Timeout errors
  - Example: `Request timeout: GET /calls - Failed after 30s`

### Advanced Logging Configuration

#### Logging to a File

```python
import logging
from aircall import AircallClient

# Configure file logging
logging.basicConfig(
    filename='aircall_api.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

client = AircallClient(api_id="your_id", api_token="your_token")
```

#### Custom Logger Configuration

```python
import logging
from aircall import AircallClient

# Create custom logger with specific handler
logger = logging.getLogger('aircall')
logger.setLevel(logging.INFO)

# Add console handler
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

# Custom formatter
formatter = logging.Formatter(
    '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

client = AircallClient(api_id="your_id", api_token="your_token")
```

#### Filtering Logs by Resource

Each resource has its own logger namespace:

```python
import logging

# Only show logs from the call resource
logging.getLogger('aircall.resources.CallResource').setLevel(logging.DEBUG)

# Disable logging for the contact resource
logging.getLogger('aircall.resources.ContactResource').setLevel(logging.CRITICAL)
```

### Example Log Output

With `verbose=True` or `DEBUG` level logging enabled:

```
2025-11-09 10:30:45 - aircall.client - INFO - Aircall client initialized
2025-11-09 10:30:46 - aircall.client - DEBUG - Request: GET https://api.aircall.io/v1/numbers
2025-11-09 10:30:46 - aircall.client - DEBUG -   Query params: {'page': 1, 'per_page': 20}
2025-11-09 10:30:46 - aircall.client - DEBUG - Response: 200 GET https://api.aircall.io/v1/numbers (took 0.23s)
2025-11-09 10:30:47 - aircall.resources.CallResource - INFO - Transferring call 12345 to number 67890
2025-11-09 10:30:47 - aircall.client - DEBUG - Request: POST https://api.aircall.io/v1/calls/12345/transfers
2025-11-09 10:30:47 - aircall.client - DEBUG -   Request body: {'number_id': 67890}
2025-11-09 10:30:48 - aircall.client - DEBUG - Response: 200 POST https://api.aircall.io/v1/calls/12345/transfers (took 0.45s)
2025-11-09 10:30:48 - aircall.resources.CallResource - INFO - Successfully transferred call 12345
```

### Best Practices

1. **Production**: Use `INFO` or `WARNING` level to avoid logging sensitive request/response data
2. **Development**: Use `DEBUG` level or `verbose=True` for detailed troubleshooting
3. **Monitoring**: Use `WARNING` level to track API errors and rate limits
4. **File Logging**: Always use file logging in production for audit trails
5. **Sensitive Data**: Be cautious about logging request bodies that might contain PII

## Development

### Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/yourusername/aircall-api.git
cd aircall-api

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### Testing

```bash
# Run the test suite
uv run pytest

# Run tests with coverage
uv run pytest --cov=aircall
```

Tests run entirely offline: a recording stand-in replaces the HTTP session, and the
response fixtures in `tests/payloads.py` are transcribed from Aircall's own published
examples, so the models are tested against what Aircall documents returning.

### Linting

```bash
# Run ruff for linting
ruff check .

# Run pylint
pylint src/aircall
```

## Project Structure

```
aircall-api/
├── src/
│   └── aircall/
│       ├── __init__.py
│       ├── client.py          # Main API client
│       ├── exceptions.py      # Custom exceptions
│       ├── pagination.py      # Page and PageMeta
│       ├── deprecation.py     # Deprecation warnings
│       ├── models/            # Pydantic models
│       │   ├── call.py
│       │   ├── contact.py
│       │   ├── user.py
│       │   └── ...
│       └── resources/         # API resource handlers
│           ├── base.py
│           ├── call.py
│           ├── contact.py
│           └── ...
├── tests/                     # Test suite
├── pyproject.toml            # Project configuration
└── README.md
```

## Requirements

- Python >= 3.13
- requests >= 2.32.5
- pydantic >= 2.12.4

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Resources

- [Aircall API Documentation](https://developers.aircall.io/api-references)
- [Migration guide: 1.x to 2.0](MIGRATION.md)
- [Aircall Dashboard](https://dashboard.aircall.io)

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/yourusername/aircall-api/issues)
- Check the [Aircall API Documentation](https://developer.aircall.io/)