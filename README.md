# URL Shortener with Analytics (Flask)

A backend URL shortening service built using Flask and SQLite.  
The system converts long URLs into short Base62-encoded links, supports redirection, and tracks usage analytics.

## Features
- Shortens long URLs into compact Base62 codes
- Redirects short URLs to original destinations
- Tracks click counts for each URL
- Persists data using SQLite
- Implements in-memory caching for faster redirects
- Provides analytics endpoint for URL statistics

## API Endpoints

### Create Short URL
`POST /shorten`

Request:
```json
{
  "url": "https://example.com"
}
Response:
{
  "short_url": "http://localhost:8000/abc123"
}

