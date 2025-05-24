# Postman Guide for GitHub Repository Discovery & Scraping Service

This guide provides comprehensive examples for testing the GitHub Repository Discovery & Scraping Service using Postman.

## Quick Setup

### 1. Import the Collection

1. Open Postman
2. Click "Import" button
3. Select the `postman_collection.json` file from this project
4. The collection will be imported with all pre-configured requests

### 2. Environment Variables

The collection uses a variable `{{base_url}}` which is set to `http://localhost:8000` by default.

To modify the base URL:

1. Go to the collection settings
2. Click on "Variables" tab
3. Update the `base_url` value if needed

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /health`
**Purpose:** Check if the service is running

```
GET http://localhost:8000/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "service": "GitHub Repository Discovery & Scraping Service"
}
```

### 2. Root Endpoint

**Endpoint:** `GET /`
**Purpose:** Get basic service information

```
GET http://localhost:8000/
```

**Expected Response:**

```json
{
  "message": "GitHub Repository Discovery & Scraping Service"
}
```

### 3. Discover Repositories

**Endpoint:** `GET /discover`
**Purpose:** Search for GitHub repositories based on criteria

## Discovery Query Parameters

| Parameter   | Type          | Default | Description                            | Example                    |
| ----------- | ------------- | ------- | -------------------------------------- | -------------------------- |
| `min_stars` | integer       | 0       | Minimum number of stars                | `1000`                     |
| `min_forks` | integer       | 0       | Minimum number of forks                | `500`                      |
| `languages` | array[string] | null    | Programming languages to filter by     | `["Python", "JavaScript"]` |
| `top_k`     | integer       | 10      | Maximum number of repositories (1-100) | `25`                       |
| `sort`      | string        | "stars" | Sort by: stars, forks, or updated      | `"forks"`                  |

### 4. Scrape Repository

**Endpoint:** `POST /scrape`
**Purpose:** Scrape code snippets from a GitHub repository

## Scraping Request Body

```json
{
  "repo_url": "https://github.com/owner/repo",
  "mode": "files",
  "start_year": 2024,
  "end_year": 2024,
  "top_k": 10
}
```

## Scraping Parameters

| Parameter    | Type    | Required | Default | Description                            | Example                                   |
| ------------ | ------- | -------- | ------- | -------------------------------------- | ----------------------------------------- |
| `repo_url`   | string  | Yes      | -       | GitHub repository URL                  | `"https://github.com/fastapi/fastapi"`    |
| `mode`       | string  | Yes      | -       | Scraping mode                          | `"files"`, `"commits"`, `"pull_requests"` |
| `start_year` | integer | No       | null    | Start year for time window (2008-2025) | `2024`                                    |
| `end_year`   | integer | No       | null    | End year for time window (2008-2025)   | `2024`                                    |
| `top_k`      | integer | No       | 10      | Maximum code samples to return (1-100) | `5`                                       |

## Scraping Modes

| Mode            | Description                      | Use Case                                  |
| --------------- | -------------------------------- | ----------------------------------------- |
| `files`         | Scrape source code files         | Get current codebase structure            |
| `commits`       | Scrape code changes from commits | Analyze code evolution and changes        |
| `pull_requests` | Scrape code changes from PRs     | Review code contributions and discussions |

## Example Requests

### Discovery Examples

#### Example 1: Popular Python Repositories

```
GET http://localhost:8000/discover?min_stars=1000&languages=Python&top_k=5&sort=stars
```

**Use Case:** Find the top 5 most starred Python repositories with at least 1000 stars.

#### Example 2: JavaScript/TypeScript Repositories

```
GET http://localhost:8000/discover?min_stars=500&languages=JavaScript&languages=TypeScript&top_k=15&sort=forks
```

**Use Case:** Find JavaScript or TypeScript repositories with at least 500 stars, sorted by fork count.

#### Example 3: Recently Updated Go Repositories

```
GET http://localhost:8000/discover?min_stars=100&languages=Go&top_k=20&sort=updated
```

**Use Case:** Find recently updated Go repositories with at least 100 stars.

### Scraping Examples

#### Example 1: Scrape Source Files

```json
{
  "repo_url": "https://github.com/fastapi/fastapi",
  "mode": "files",
  "top_k": 3
}
```

**Use Case:** Get source code files from the FastAPI repository.

#### Example 2: Scrape Recent Commits

```json
{
  "repo_url": "https://github.com/fastapi/fastapi",
  "mode": "commits",
  "start_year": 2024,
  "end_year": 2024,
  "top_k": 5
}
```

**Use Case:** Get code changes from 2024 commits.

#### Example 3: Scrape Pull Requests

```json
{
  "repo_url": "https://github.com/tiangolo/typer",
  "mode": "pull_requests",
  "start_year": 2024,
  "top_k": 3
}
```

**Use Case:** Get code changes from recent pull requests.

#### Example 4: Scrape with Time Window

```json
{
  "repo_url": "https://github.com/fastapi/fastapi",
  "mode": "commits",
  "start_year": 2023,
  "end_year": 2023,
  "top_k": 10
}
```

**Use Case:** Get all commits from 2023 only.

## Response Formats

### Discovery Response

```json
{
  "repositories": [
    {
      "name": "repository-name",
      "full_name": "owner/repository-name",
      "description": "Repository description",
      "html_url": "https://github.com/owner/repository-name",
      "stars": 12345,
      "forks": 6789,
      "language": "Python",
      "created_at": "2020-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "owner": {
        "login": "owner-username",
        "id": 12345,
        "avatar_url": "https://avatars.githubusercontent.com/u/12345",
        "type": "User"
      }
    }
  ],
  "total_count": 1000000,
  "search_criteria": {
    "min_stars": 1000,
    "min_forks": 0,
    "languages": ["Python"],
    "top_k": 10,
    "sort": "stars"
  }
}
```

### Scraping Response

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

## Testing Scenarios

### 1. Basic Functionality Test

1. **Health Check** - Verify service is running
2. **Root Endpoint** - Check basic service info
3. **Default Discovery** - Test with no parameters
4. **Basic Scraping** - Test each scraping mode

### 2. Discovery Parameter Validation Tests

1. **Minimum Stars** - Test different star thresholds
2. **Minimum Forks** - Test different fork thresholds
3. **Language Filtering** - Test single and multiple languages
4. **Sorting Options** - Test all sort options (stars, forks, updated)
5. **Result Limits** - Test different top_k values

### 3. Scraping Parameter Validation Tests

1. **All Modes** - Test files, commits, and pull_requests modes
2. **Time Windows** - Test different start_year and end_year combinations
3. **Repository Validation** - Test with valid and invalid URLs
4. **Result Limits** - Test different top_k values for scraping

### 4. Edge Cases

1. **No Results** - Search/scrape with very high thresholds
2. **Maximum Limits** - Test with top_k=100
3. **Invalid Parameters** - Test with invalid values
4. **Empty Repositories** - Test scraping empty repositories
5. **Private Repositories** - Test scraping private repos (should fail)

### 5. Performance Tests

1. **Large Result Sets** - Request maximum repositories/snippets
2. **Multiple Languages** - Test with many language filters
3. **Response Time** - Monitor API response times
4. **Concurrent Requests** - Test multiple simultaneous requests

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK** - Successful request
- **404 Not Found** - Repository not found
- **422 Unprocessable Entity** - Invalid parameters
- **429 Too Many Requests** - GitHub API rate limit exceeded
- **503 Service Unavailable** - GitHub API connection issues
- **504 Gateway Timeout** - Request timeout

## Tips for Testing

1. **Rate Limiting**: GitHub API has rate limits. If you get 429 errors, wait before retrying.

2. **Language Names**: Use exact language names as they appear on GitHub (e.g., "JavaScript", "TypeScript", "C++").

3. **URL Encoding**: Special characters in language names (like C++) are automatically URL encoded in Postman.

4. **Repository URLs**: Use full GitHub URLs (e.g., `https://github.com/owner/repo`).

5. **Time Windows**: Use realistic year ranges (2008-2025) for filtering.

6. **Content Size**: Scraped content can be large; consider using smaller top_k values for testing.

## Collection Structure

The imported Postman collection includes:

### Discovery Endpoints

1. **Health Check** - Service health verification
2. **Root Endpoint** - Basic service info
3. **Discover Popular Python Repositories** - Python-specific search
4. **Discover JavaScript/TypeScript Repositories** - Multi-language search
5. **Discover Recently Updated Go Repositories** - Sort by update time

### Scraping Endpoints

6. **Scrape Files Mode** - Get source code files
7. **Scrape Commits Mode** - Get commit changes
8. **Scrape Pull Requests Mode** - Get PR changes
9. **Scrape with Time Window** - Time-filtered scraping
10. **Scrape Error Case** - Test invalid repository

Each request includes detailed descriptions and properly configured parameters for easy testing.
