# Contributing to Aircall API

Thank you for your interest in contributing to the Aircall API Python client! We welcome contributions from the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up your development environment
4. Create a new branch for your changes
5. Make your changes
6. Submit a pull request

## Development Setup

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

### Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) installed

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/aircall-api.git
cd aircall-api

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies (including dev dependencies)
uv sync --dev

# Activate the virtual environment
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

## Making Changes

### Branch Naming

Use descriptive branch names that indicate the type of change:

- `feature/add-new-endpoint` - New features
- `fix/authentication-bug` - Bug fixes
- `docs/update-readme` - Documentation updates
- `refactor/simplify-client` - Code refactoring

### Commit Messages

Write clear, concise commit messages:

```
feat: Add support for AI Voice Agents endpoint

- Implement AIVoiceAgentResource class
- Add Pydantic models for agents
- Update client to include new resource
```

Use conventional commit prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

## Code Style

This project follows strict code quality standards.

### Linting

We use two linters that must pass before merging:

```bash
# Run pylint
uv run pylint --ignore=__pycache__ \
              --max-line-length=120 \
              --fail-under=8 \
              src/aircall/

# Run ruff
uv run ruff check src/
```

### Style Guidelines

- **Maximum line length**: 120 characters
- **Type hints**: Use type hints for all function parameters and return values
- **Docstrings**: Add docstrings to all public classes and methods
- **Imports**: Group imports (standard library, third-party, local)
- **Naming conventions**:
  - Classes: `PascalCase`
  - Functions/methods: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private attributes: `_leading_underscore`

### Example Code Style

```python
from typing import Optional, Dict, Any

from pydantic import BaseModel


class Contact(BaseModel):
    """Represents an Aircall contact.

    Attributes:
        id: Unique identifier for the contact
        first_name: Contact's first name
        last_name: Contact's last name
    """

    id: int
    first_name: str
    last_name: Optional[str] = None

    def get_full_name(self) -> str:
        """Returns the contact's full name.

        Returns:
            The full name as a string
        """
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
```

## Testing

**Currently, this project does not have a test suite.** We welcome and encourage community contributions to help build comprehensive test coverage! If you're interested in contributing tests, this would be an excellent way to help the project.

### Guidelines for Contributing Tests

- Use pytest as the testing framework
- Place tests in the `tests/` directory, mirroring the source structure
- Use descriptive test names
- Mock external API calls (don't make real API requests in tests)
- Test both success and error cases
- Include edge cases and error handling

**Areas that would benefit from tests:**
- Client initialization and authentication
- All resource endpoints (calls, contacts, numbers, etc.)
- Error handling and custom exceptions
- Request/response serialization
- Pagination handling
- Logging functionality

## Submitting Changes

### Pull Request Process

1. **Update your branch** with the latest changes from `main`:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run linters** to ensure code quality:
   ```bash
   uv run pylint src/aircall/
   uv run ruff check src/
   ```

3. **Push your changes** to your fork:
   ```bash
   git push origin your-branch-name
   ```

4. **Open a Pull Request** on GitHub:
   - Use a clear, descriptive title
   - Fill out the PR template completely
   - Link any related issues
   - Describe what changed and why

5. **Respond to feedback**:
   - Address review comments promptly
   - Update your PR as needed
   - Be open to suggestions

### PR Checklist

Before submitting, ensure:

- [ ] Code follows the project's style guidelines
- [ ] Linters pass (pylint and ruff)
- [ ] All tests pass (if applicable)
- [ ] Documentation is updated (if needed)
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes
- [ ] No merge conflicts with main branch

## Reporting Issues

### Bug Reports

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml) and include:

- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Code sample demonstrating the issue
- Version information (package, Python, OS)

### Feature Requests

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml) and include:

- Description of the problem you're trying to solve
- Proposed solution
- Alternative solutions considered
- Code examples of how you'd like to use the feature

## Development Tips

### Testing Against the Real API

If you have Aircall API credentials, you can test against the real API:

```python
from aircall import AircallClient

# Use test credentials
client = AircallClient(
    api_id="your_test_api_id",
    api_token="your_test_api_token",
    verbose=True  # Enable debug logging
)

# Make API calls
numbers = client.number.list()
```

**Important**: Never commit real API credentials! Use environment variables:

```python
import os
from aircall import AircallClient

client = AircallClient(
    api_id=os.getenv("AIRCALL_API_ID"),
    api_token=os.getenv("AIRCALL_API_TOKEN")
)
```

### Debugging

Enable verbose logging to see detailed API requests/responses:

```python
from aircall import AircallClient

client = AircallClient(
    api_id="...",
    api_token="...",
    verbose=True  # Enables DEBUG logging
)
```

## Questions?

If you have questions or need help:

- Open a [Discussion](https://github.com/Riprock/aircall-api/discussions)
- Check the [Aircall API Documentation](https://developer.aircall.io/)
- Review existing [Issues](https://github.com/Riprock/aircall-api/issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Aircall API! 🚀