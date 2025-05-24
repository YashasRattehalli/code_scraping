# Postman Guide for GitHub Repository Discovery Service

This guide provides comprehensive examples for testing the GitHub Repository Discovery Service using Postman.

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
  "service": "GitHub Repository Discovery Service"
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
  "message": "GitHub Repository Discovery Service"
}
```

### 3. Discover Repositories

**Endpoint:** `GET /discover`
**Purpose:** Search for GitHub repositories based on criteria

## Query Parameters

| Parameter   | Type          | Default | Description                            | Example                    |
| ----------- | ------------- | ------- | -------------------------------------- | -------------------------- |
| `min_stars` | integer       | 0       | Minimum number of stars                | `1000`                     |
| `min_forks` | integer       | 0       | Minimum number of forks                | `500`                      |
| `languages` | array[string] | null    | Programming languages to filter by     | `["Python", "JavaScript"]` |
| `top_k`     | integer       | 10      | Maximum number of repositories (1-100) | `25`                       |
| `sort`      | string        | "stars" | Sort by: stars, forks, or updated      | `"forks"`                  |

## Example Requests

### Example 1: Popular Python Repositories

```
GET http://localhost:8000/discover?min_stars=1000&languages=Python&top_k=5&sort=stars
```

**Use Case:** Find the top 5 most starred Python repositories with at least 1000 stars.

### Example 2: JavaScript/TypeScript Repositories

```
GET http://localhost:8000/discover?min_stars=500&languages=JavaScript&languages=TypeScript&top_k=15&sort=forks
```

**Use Case:** Find JavaScript or TypeScript repositories with at least 500 stars, sorted by fork count.

### Example 3: Recently Updated Go Repositories

```
GET http://localhost:8000/discover?min_stars=100&languages=Go&top_k=20&sort=updated
```

**Use Case:** Find recently updated Go repositories with at least 100 stars.

### Example 4: High Fork Count Repositories

```
GET http://localhost:8000/discover?min_forks=1000&top_k=25&sort=forks
```

**Use Case:** Find repositories with at least 1000 forks, regardless of language.

### Example 5: Multiple Programming Languages

```
GET http://localhost:8000/discover?min_stars=200&languages=Python&languages=Java&languages=C%2B%2B&top_k=30&sort=stars
```

**Use Case:** Find repositories in Python, Java, or C++ with at least 200 stars.

### Example 6: Default Parameters

```
GET http://localhost:8000/discover
```

**Use Case:** Use default parameters to get a general list of repositories.

## Response Format

All `/discover` endpoints return the following JSON structure:

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

## Testing Scenarios

### 1. Basic Functionality Test

1. **Health Check** - Verify service is running
2. **Root Endpoint** - Check basic service info
3. **Default Discovery** - Test with no parameters

### 2. Parameter Validation Tests

1. **Minimum Stars** - Test different star thresholds
2. **Minimum Forks** - Test different fork thresholds
3. **Language Filtering** - Test single and multiple languages
4. **Sorting Options** - Test all sort options (stars, forks, updated)
5. **Result Limits** - Test different top_k values

### 3. Edge Cases

1. **No Results** - Search with very high thresholds
2. **Maximum Limit** - Test with top_k=100
3. **Invalid Parameters** - Test with invalid sort values
4. **Special Characters** - Test languages with special characters (C++)

### 4. Performance Tests

1. **Large Result Sets** - Request maximum repositories
2. **Multiple Languages** - Test with many language filters
3. **Response Time** - Monitor API response times

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK** - Successful request
- **422 Unprocessable Entity** - Invalid parameters
- **429 Too Many Requests** - GitHub API rate limit exceeded
- **503 Service Unavailable** - GitHub API connection issues
- **504 Gateway Timeout** - Request timeout

## Tips for Testing

1. **Rate Limiting**: GitHub API has rate limits. If you get 429 errors, wait before retrying.

2. **Language Names**: Use exact language names as they appear on GitHub (e.g., "JavaScript", "TypeScript", "C++").

3. **URL Encoding**: Special characters in language names (like C++) are automatically URL encoded in Postman.

4. **Multiple Values**: To test multiple languages, add multiple `languages` parameters in Postman's query params section.

5. **Response Validation**: Check that the returned repositories match your search criteria.

## Collection Structure

The imported Postman collection includes:

1. **Health Check** - Service health verification
2. **Root Endpoint** - Basic service info
3. **Discover Popular Python Repositories** - Python-specific search
4. **Discover JavaScript/TypeScript Repositories** - Multi-language search
5. **Discover Recently Updated Go Repositories** - Sort by update time
6. **Discover High Fork Count Repositories** - Fork-based filtering
7. **Discover Rust Repositories** - Rust-specific search
8. **Discover Multiple Languages** - Multi-language filtering
9. **Discover Any Popular Repositories** - High star count, any language
10. **Minimal Query** - Default parameters test

Each request includes detailed descriptions and properly configured parameters for easy testing.
