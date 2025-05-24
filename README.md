# GitHub Repository Discovery & Scraping Service

A FastAPI-based service for discovering GitHub repositories and scraping code snippets based on various criteria such as stars, forks, programming languages, and time windows.

## Features

- 🔍 **Repository Discovery**: Search repositories by minimum stars and forks
- 🏷️ **Language Filtering**: Filter by programming languages
- 📊 **Flexible Sorting**: Sort by stars, forks, or last updated date
- 🛠️ **Code Scraping**: Extract code snippets from repositories
- 📂 **Multiple Scraping Modes**: Files, commits, and pull requests
- ⏰ **Time Window Filtering**: Filter by date ranges for commits and PRs
- 🚀 **Fast and Scalable**: FastAPI backend with async support
- 📝 **Comprehensive API Documentation**: Auto-generated OpenAPI docs
- 🛡️ **Built-in Error Handling**: Rate limiting awareness and proper error responses

## Quick Start

### Prerequisites

- Python 3.9+
- `uv` package manager (will be installed automatically if not present)

### Installation and Setup

1. **Clone the repository and navigate to the project directory**

2. **Set up the environment and install dependencies:**

   ```bash
   make install
   ```

3. **Start the development server:**
   ```bash
   make dev
   ```

The API will be available at `http://localhost:8000`

### Available Make Commands

- `make setup` - Install uv and create virtual environment
- `make install` - Install all dependencies
- `make dev` - Start development server with auto-reload
- `make run` - Start production server
- `make clean` - Remove virtual environment

## API Endpoints

### 🔍 Repository Discovery

**GET** `/discover`

Discover GitHub repositories based on specified criteria.

#### Query Parameters

| Parameter   | Type      | Default | Description                             |
| ----------- | --------- | ------- | --------------------------------------- |
| `min_stars` | int       | 0       | Minimum number of stars                 |
| `min_forks` | int       | 0       | Minimum number of forks                 |
| `languages` | List[str] | None    | Programming languages to filter by      |
| `top_k`     | int       | 10      | Maximum repositories to return (1-100)  |
| `sort`      | str       | "stars" | Sort by: "stars", "forks", or "updated" |

#### Example Requests

```bash
# Find popular Python repositories
curl "http://localhost:8000/discover?min_stars=1000&languages=Python&top_k=5"

# Find JavaScript/TypeScript repos with many forks
curl "http://localhost:8000/discover?min_forks=500&languages=JavaScript&languages=TypeScript&sort=forks"

# Find recently updated Go repositories
curl "http://localhost:8000/discover?min_stars=100&languages=Go&sort=updated"
```

#### Discovery Response Format

```json
{
  "repositories": [
    {
      "name": "repository-name",
      "full_name": "owner/repository-name",
      "description": "Repository description",
      "html_url": "https://github.com/owner/repository-name",
      "stars": 12345,
      "forks": 2345,
      "language": "Python",
      "created_at": "2020-01-01T00:00:00Z",
      "updated_at": "2023-12-01T00:00:00Z",
      "owner": {
        "login": "owner",
        "avatar_url": "https://avatars.githubusercontent.com/u/123456"
      }
    }
}
```

### 🛠️ Repository Scraping

**POST** `/scrape`

Scrape code snippets from GitHub repositories with different modes and filtering options.

#### Request Body Parameters

| Parameter    | Type   | Required | Default | Description                                  |
| ------------ | ------ | -------- | ------- | -------------------------------------------- |
| `repo_url`   | string | Yes      | -       | GitHub repository URL                        |
| `mode`       | string | Yes      | -       | Scraping mode: files, commits, pull_requests |
| `start_year` | int    | No       | null    | Start year for time window (2008-2025)       |
| `end_year`   | int    | No       | null    | End year for time window (2008-2025)         |
| `top_k`      | int    | No       | 10      | Maximum code samples to return (1-100)       |

#### Scraping Modes

| Mode            | Description                      | Use Case                                  |
| --------------- | -------------------------------- | ----------------------------------------- |
| `files`         | Scrape source code files         | Get current codebase structure            |
| `commits`       | Scrape code changes from commits | Analyze code evolution and changes        |
| `pull_requests` | Scrape code changes from PRs     | Review code contributions and discussions |

#### Example Scraping Requests

```bash
# Scrape source files from FastAPI repository
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/fastapi/fastapi",
    "mode": "files",
    "top_k": 3
  }'

# Scrape recent commits with time window
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/fastapi/fastapi",
    "mode": "commits",
    "start_year": 2024,
    "end_year": 2024,
    "top_k": 5
  }'

# Scrape pull requests
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/tiangolo/typer",
    "mode": "pull_requests",
    "start_year": 2024,
    "top_k": 3
  }'
```

#### Scraping Response Format

```json
{
  "repository": {
    "name": "fastapi",
    "full_name": "fastapi/fastapi",
    "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
    "language": "Python",
    "stars": 84985,
    "forks": 7358,
    "created_at": "2018-12-08T08:21:47Z",
    "updated_at": "2025-05-24T14:30:41Z"
  },
  "mode": "files",
  "time_window": {
    "start_year": 2024,
    "end_year": 2024
  },
  "code_snippets": [
    {
      "content": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get(\"/\")\ndef read_root():\n    return {\"Hello\": \"World\"}",
      "file_path": "main.py",
      "language": "Python",
      "size_bytes": 128,
      "lines_count": 7,
      "commit_sha": "abc123...",
      "commit_message": "Initial commit",
      "commit_date": "2024-01-01T00:00:00Z",
      "author": "John Doe",
      "pr_number": 123,
      "pr_title": "Add main endpoint"
    }
  ],
  "total_found": 50,
  "returned_count": 3
}
```

### 🏥 Health Check

**GET** `/health`

Check if the service is running properly.

```bash
curl "http://localhost:8000/health"
```

## Testing the API

### Quick Tests with cURL

```bash
# Test repository discovery
curl "http://localhost:8000/discover?min_stars=1000&languages=Python&top_k=3"

# Test file scraping
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/fastapi/fastapi", "mode": "files", "top_k": 2}'

# Test commit scraping
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/fastapi/fastapi", "mode": "commits", "start_year": 2024, "top_k": 2}'
```

### Using the Test Scripts

```bash
# Make sure the server is running first
make dev

# Run the curl test script (if available)
./test_scraper_curl.sh
```

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON schema**: http://localhost:8000/openapi.json

## Error Handling

The API handles various error scenarios:

- **404 Not Found**: Repository not found
- **422 Unprocessable Entity**: Invalid parameters or request body
- **429 Too Many Requests**: GitHub API rate limit exceeded
- **503 Service Unavailable**: GitHub API connection issues
- **504 Gateway Timeout**: Request timeout

## Rate Limits

The service uses the GitHub API, which has rate limits:

- **Unauthenticated requests**: 60 requests per hour per IP
- **Authenticated requests**: 5,000 requests per hour (requires GitHub token)

To use authenticated requests, set the `GITHUB_TOKEN` environment variable.

## Development

### Project Structure

```
.
├── app/
│   ├── endpoints/          # API endpoints
│   │   ├── repositories.py # Discovery endpoints
│   │   ├── scraper.py     # Scraping endpoints
│   │   └── health.py      # Health check
│   ├── services/          # Business logic
│   │   ├── github_service.py     # Repository discovery
│   │   └── scraper_service.py    # Code scraping
│   ├── schemas/           # Pydantic models
│   │   ├── repository.py  # Discovery schemas
│   │   └── scraper.py     # Scraping schemas
│   └── main.py           # FastAPI application
├── POSTMAN_GUIDE.md      # Postman testing guide
├── pyproject.toml        # Project dependencies
├── Makefile             # Build and run commands
└── README.md            # This file
```

### Adding Features

The service is designed to be modular and extensible. You can easily add:

- **Authentication**: GitHub tokens for higher rate limits
- **Caching**: Redis/in-memory caching for improved performance
- **Additional Search Criteria**: More repository filters
- **Database Storage**: Store search/scraping history
- **Background Tasks**: Bulk operations and async processing
- **Content Analysis**: Code complexity metrics, language statistics
- **Export Formats**: CSV, JSON, or ZIP downloads

## Use Cases

### Repository Discovery

- **Research**: Find popular repositories in specific languages
- **Competition Analysis**: Discover trending projects
- **Learning**: Find well-maintained examples and tutorials
- **Recruitment**: Identify active developers and projects

### Code Scraping

- **Code Analysis**: Study coding patterns and practices
- **Documentation**: Extract examples for documentation
- **Migration**: Analyze codebases before modernization
- **Security**: Review code changes in commits/PRs
- **Learning**: Study real-world implementations

## License

This project is open source and available under the MIT License.
