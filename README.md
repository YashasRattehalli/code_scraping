# GitHub Repository Discovery Service

A FastAPI-based service for discovering GitHub repositories based on various criteria such as stars, forks, and programming languages.

## Features

- 🔍 Search repositories by minimum stars and forks
- 🏷️ Filter by programming languages
- 📊 Sort by stars, forks, or last updated date
- 🚀 Fast and scalable FastAPI backend
- 📝 Comprehensive API documentation
- 🛡️ Built-in error handling and rate limiting awareness

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

#### Response Format

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
  ],
  "total_count": 1000,
  "search_criteria": {
    "min_stars": 1000,
    "min_forks": 0,
    "languages": ["Python"],
    "top_k": 5,
    "sort": "stars"
  }
}
```

### 🏥 Health Check

**GET** `/health`

Check if the service is running properly.

```bash
curl "http://localhost:8000/health"
```

## Testing the API

Run the example script to test various API endpoints:

```bash
# Make sure the server is running first
make dev

# In another terminal, run the example
python example_usage.py
```

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI JSON schema**: http://localhost:8000/openapi.json

## Error Handling

The API handles various error scenarios:

- **Rate Limiting**: Returns 429 when GitHub API rate limit is exceeded
- **Timeouts**: Returns 504 for request timeouts
- **Connection Issues**: Returns 503 for connection problems
- **Invalid Parameters**: Returns 422 for validation errors

## Rate Limits

The service uses the GitHub API, which has rate limits:

- **Unauthenticated requests**: 60 requests per hour per IP
- **Authenticated requests**: 5,000 requests per hour (requires GitHub token)

To use authenticated requests, set the `GITHUB_TOKEN` environment variable.

## Development

### Project Structure

```
.
├── main.py              # FastAPI application
├── example_usage.py     # Example API usage
├── pyproject.toml       # Project dependencies
├── Makefile            # Build and run commands
└── README.md           # This file
```

### Adding Features

The service is designed to be modular and extensible. You can easily add:

- Authentication with GitHub tokens
- Caching for improved performance
- Additional search criteria
- Database storage for search history
- Background tasks for bulk operations

## License

This project is open source and available under the MIT License.
