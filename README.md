# RobotXT Parser

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Type Checking](https://img.shields.io/badge/type%20checking-mypy-blue)](https://github.com/python/mypy)

A robust Python library for parsing and analyzing robots.txt files according to Google's guidelines. This library provides a simple interface for web crawlers to check if they are allowed to access specific paths on a website.

## Features

- 🚀 Fast and efficient robots.txt parsing
- 🔒 Follows Google's robots.txt specification
- 🌐 Support for both HTTP and HTTPS
- 📊 Comprehensive rule evaluation
- 🔄 Built-in caching mechanism
- 📝 Detailed logging
- 🧪 Extensive test coverage
- 🔍 Support for wildcard patterns
- ⏱️ Crawl delay parsing
- 🗺️ Sitemap extraction

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/robotxt-parser.git
cd robotxt-parser

# Create and activate virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .
```

## Quick Start

### As a Library

```python
from robotxt_parser import RobotParser

# Initialize parser
parser = RobotParser()

# Set the URL to analyze
url = "https://example.com"
parser.set_url(url)

# Check if a path is allowed for a specific user-agent
user_agent = "MyBot"
path = "/some/path"
is_allowed = parser.check_for_rule(user_agent, path)
print(f"Path {path} is {'allowed' if is_allowed else 'disallowed'} for {user_agent}")

# Get all sitemaps
sitemaps = parser.get_sitemaps()
print("Sitemaps:", sitemaps)

# Get crawl delay
delay = parser.get_crawl_delay(user_agent)
print(f"Crawl delay for {user_agent}: {delay}")
```

### As a Command-Line Tool

```bash
# Check if a path is allowed
robotxt https://example.com --user-agent MyBot --path /some/path

# Get all sitemaps
robotxt https://example.com --action sitemaps

# Get crawl delay
robotxt https://example.com --action crawl_delay --user-agent MyBot

# Enable verbose output
robotxt https://example.com --verbose
```

## API Reference

### RobotParser

Main class for parsing and evaluating robots.txt files.

#### Methods

- `set_url(url: str) -> None`
  - Set the URL to analyze
  - Args:
    - url: The URL to set

- `check_for_rule(user_agent: str, path: str) -> bool`
  - Check if a path is allowed for a specific user-agent
  - Args:
    - user_agent: The user-agent to check
    - path: The path to check
  - Returns: True if path is allowed, False otherwise

- `get_sitemaps() -> List[str]`
  - Get all sitemap URLs from robots.txt
  - Returns: List of sitemap URLs

- `get_crawl_delay(user_agent: str) -> Optional[float]`
  - Get crawl delay for a specific user-agent
  - Args:
    - user_agent: The user-agent to get crawl delay for
  - Returns: Crawl delay in seconds or None if not specified

- `parse(url: str, action: str) -> Optional[Union[Dict, List[str]]]`
  - Parse robots.txt content for specific actions
  - Args:
    - url: The URL to parse
    - action: The action to perform ('crawl_delay', 'sitemaps', 'user_agent')
  - Returns: Parsed results based on action

## Project Structure

```
robotxt_parser/
├── src/
│   └── robotxt_parser/
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── robot_parser.py
│       │   └── exceptions.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── url_utils.py
│       ├── cli/
│       │   ├── __init__.py
│       │   └── main.py
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_robot_parser.py
├── examples/
│   └── basic_usage.py
├── README.md
├── setup.py
└── requirements.txt
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=robotxt_parser

# Run tests with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black .

# Sort imports
isort .

# Type checking
mypy .

# Linting
flake8
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built following [Google's robots.txt specifications](https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt)
- Inspired by the Python community's best practices
- Uses the [Requests](https://docs.python-requests.org/) library for HTTP requests
