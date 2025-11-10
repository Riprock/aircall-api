# Aircall API

A Python client library for the [Aircall.io](https://aircall.io) API, providing easy access to Aircall's telephony services.

## Features

- Full type hints with Pydantic models
- Comprehensive API coverage for Aircall endpoints
- Simple and intuitive interface
- Built-in authentication handling
- Custom exceptions for proper error handling
- Automatic request/response serialization
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

# Initialize the client
client = AircallClient(
    api_id="your_api_id",
    api_token="your_api_token"
)

# List phone numbers
numbers = client.number.list()

# Get a specific number
number = client.number.get(12345)
```

## Authentication

To use this library, you'll need your Aircall API credentials:

1. Log in to your [Aircall Dashboard](https://dashboard.aircall.io)
2. Navigate to Settings > Integrations > API Keys
3. Create a new API key or use an existing one
4. Use the API ID and API Token to initialize the client

```python
client = AircallClient(
    api_id="YOUR_API_ID",
    api_token="YOUR_API_TOKEN",
    timeout=30,  # Optional: request timeout in seconds
    verbose=False  # Optional: enable debug logging
)
```

## Available Resources

The library provides access to the following Aircall API resources:

- **Calls** - List, search, retrieve call details, voicemails, and insights
- **Contacts** - Manage contact information
- **Numbers** - Manage phone numbers
- **Users** - Manage team members
- **Teams** - Manage teams
- **Tags** - Organize calls and contacts with tags
- **Messages** - SMS messaging
- **Webhooks** - Configure webhook endpoints
- **Integrations** - Manage third-party integrations
- **Dialer Campaigns** - Manage dialer campaigns
- **Companies** - Company information
- **AI Voice Agents** - AI-powered voice agent management
- **Conversation Intelligence** - Call analytics and insights

### Usage Examples

#### Working with Calls

```python
# List all calls
calls = client.call.list(page=1, per_page=20)

# Get a specific call
call = client.call.get(call_id=12345)

# Search for calls
calls = client.call.search(from_date="2024-01-01", to_date="2024-01-31")
```

#### Working with Contacts

```python
# List all contacts
contacts = client.contact.list()

# Create a new contact
contact = client.contact.create(
    first_name="John",
    last_name="Doe",
    phone_numbers=["+1234567890"]
)

# Update a contact
client.contact.update(contact_id=12345, email="john.doe@example.com")
```

#### Working with Numbers

```python
# List all numbers
numbers = client.number.list()

# Get a specific number
number = client.number.get(number_id=12345)
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
numbers = client.number.list()
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
# Run tests
pytest

# Run tests with coverage
pytest --cov=aircall
```

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

- [Aircall API Documentation](https://developer.aircall.io/)
- [Aircall Dashboard](https://dashboard.aircall.io)

## Support

For issues and questions:
- Open an issue on [GitHub](https://github.com/yourusername/aircall-api/issues)
- Check the [Aircall API Documentation](https://developer.aircall.io/)