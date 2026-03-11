# URL Shortener with Analytics (Flask)

A backend URL shortening service built using **Flask** and **SQLite**.  
The system converts long URLs into compact **Base62-encoded short links**, supports redirection, and tracks **usage analytics** such as click counts.

---

## Tech Stack

- Python
- Flask
- SQLite
- REST API
- Base62 Encoding

---

## Features

- Converts long URLs into short **Base62 encoded links**
- Redirects short URLs to their original destinations
- Tracks **click counts** for each shortened URL
- Stores URL mappings in **SQLite database**
- Supports **analytics endpoint** to retrieve URL statistics
- Uses **in-memory caching** for faster redirects

---

## API Endpoints

### Create Short URL

**POST** `/shorten`

#### Request
```json
{
  "url": "https://example.com"
}
```

#### Response
```json
{
  "short_url": "http://localhost:8000/aZ91b"
}
```

---

### Redirect to Original URL

**GET** `/<short_code>`

Example:

```
http://localhost:8000/aZ91b
```

The server retrieves the original URL and performs a **302 redirect**.

---

### Get URL Statistics

**GET** `/stats/<short_code>`

Example:

```
GET /stats/aZ91b
```

#### Response

```json
{
  "url": "https://example.com",
  "clicks": 15,
  "created_at": "2026-01-20T10:30:00"
}
```

---

## How It Works

1. A user sends a URL to the `/shorten` endpoint.
2. The system generates a unique **Base62 short code**.
3. The mapping between the short code and the original URL is stored in **SQLite**.
4. When the short URL is accessed, the system retrieves the original URL.
5. The user is redirected using an **HTTP 302 redirect**.
6. Each redirect updates the **click counter** for analytics.

---

## Project Structure

```
project-root/
│
├── app.py            # Flask application and API routes
├── shortener.py      # URL shortening logic
├── database.py       # SQLite database initialization
├── urls.db           # Database file
├── requirements.txt  # Python dependencies
└── README.md
```

---

## Setup and Run

### 1. Clone the repository

```
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Run the application

```
python app.py
```

The server will start on:

```
http://localhost:8000
```

---

## Example Workflow

1. Send a POST request to `/shorten`
2. Receive a shortened URL
3. Visit the short URL to redirect to the original site
4. Use `/stats/<short_code>` to view click analytics

---

## Future Improvements

Possible enhancements:

- Custom short URLs
- Expiring links
- Rate limiting
- User authentication
- Deployment using Docker or cloud platforms

---

## Author

Built as a backend systems project to demonstrate:

- REST API design
- database integration
- backend system architecture