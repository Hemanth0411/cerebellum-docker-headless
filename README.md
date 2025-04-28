# Cerebellum Docker Headless

An AI-powered web automation framework built on top of [Cerebellum Browser Agent](https://github.com/theredsix/cerebellum), combining AI-driven automation with Selenium in a containerized environment.

## What is This Project?

This project extends the Cerebellum Browser Agent open-source framework to provide:
- Intelligent web automation using Cerebellum's AI capabilities
- State management for reliable interactions
- Dockerized execution environment
- Chrome browser integration
- Enhanced logging and debugging

### Key Components:
- **Cerebellum AI**: Provides intelligent decision-making for web interactions
- **State Tracking**: Ensures reliable form interactions and prevents redundant actions
- **Docker Integration**: Runs consistently in any environment
- **Multiple Example Scripts**: Demonstrates different use cases

### Technical Foundation
This project is built on:
- **Cerebellum Browser Agent**: The core AI-driven automation engine
- **Selenium**: Web browser automation framework
- **Chrome Browser**: Headless browser environment
- **Docker**: Containerization platform

## Use Cases

1. **Login Automation** ([login.py](login.py))
   - Automated login to web applications
   - Session token extraction
   - Login state validation
   - See [sample logs](logs-1.txt) for execution details

2. **Google Search** ([google.py](google.py))
   - Automated search queries
   - Result validation
   - Click-through automation

3. **Contact Form** ([example.py](example.py))
   - Form field detection
   - Automated form filling
   - Submission validation

## Getting Started

### Prerequisites
- Docker
- Python 3.8+
- Anthropic API key

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/Hemanth0411/cerebellum-docker-headless.git
cd cerebellum-docker-headless
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Build the Docker image:
```bash
docker build -t cerebellum-headless .
```

### Running Examples

#### 1. Login Automation
```bash
# Run the login example
docker run -it --rm \
  -e START_URL="https://example.com/login" \
  -e USERNAME="your_username" \
  -e PASSWORD="your_password" \
  -e ANTHROPIC_API_KEY="your_api_key" \
  cerebellum-headless python login.py
```

#### 2. Google Search
```bash
# Run the search example
docker run -it --rm \
  -e SEARCH_QUERY="your search query" \
  -e ANTHROPIC_API_KEY="your_api_key" \
  cerebellum-headless python google.py
```

#### 3. Contact Form
```bash
# Run the form example
docker run -it --rm \
  -e FORM_URL="https://example.com/contact" \
  -e NAME="John Doe" \
  -e EMAIL="john@example.com" \
  -e MESSAGE="Hello!" \
  -e ANTHROPIC_API_KEY="your_api_key" \
  cerebellum-headless python example.py
```

## Project Structure
```
cerebellum-docker-headless/
├── chrome-linux64/          # Chrome browser binaries
│   └── chrome               # Chrome executable
├── chromedriver-linux64/    # Chrome WebDriver
│   └── chromedriver         # WebDriver executable
├── src/
│   ├── login.py            # Login automation
│   ├── google.py           # Google search automation
│   ├── example.py          # Contact form example
│   ├── monkey_patch.py     # Action tracking patch
│   └── state_tracker.py    # State management
├── logs-1.txt              # Execution logs
├── Dockerfile              # Container configuration
├── requirements.txt        # Python dependencies
└── .env                    # Environment configuration
```

## Chrome Components
This project includes:
- **Chrome Browser**: Pre-configured headless Chrome browser (version 121.0.6167.85)
- **ChromeDriver**: WebDriver for Chrome automation (version 121.0.6167.85)
- **Automated Setup**: Chrome components are automatically configured during container build

## Environment Variables

### Common Variables
- `ANTHROPIC_API_KEY`: Your Anthropic API key for AI functionality

### Login Script Variables
- `START_URL`: Target login page URL
- `USERNAME`: Login username
- `PASSWORD`: Login password
- `API_URL`: (Optional) Endpoint to send session tokens

### Google Search Variables
- `START_URL`: Google search URL
- `SEARCH_QUERY`: Search term to look up

### Contact Form Variables
- `FORM_URL`: Contact form URL
- `NAME`: Name to enter in form
- `EMAIL`: Email to enter in form
- `MESSAGE`: Message to enter in form

## Debugging

- Check `logs-1.txt` for detailed execution logs
- Session data stored in:
  - `session_token.txt`
  - `local_storage.txt`
  - `session_storage.txt`

## Best Practices

1. Use headless mode in production
2. Set appropriate timeouts
3. Monitor state tracking logs
4. Handle failed attempts gracefully
5. Review execution logs for debugging

## Sample Execution Log
For a detailed example of how the automation works, check the [execution logs](logs-1.txt) from a successful login attempt.

## License
MIT
