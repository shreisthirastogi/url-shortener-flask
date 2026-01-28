from datetime import datetime
from urllib.parse import urlparse

from database import get_connection, init_db

BASE62 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]

    result = []
    while num > 0:
        num, rem = divmod(num, 62)
        result.append(BASE62[rem])

    return "".join(reversed(result))


def normalize_url(url: str) -> str:
  
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url


def is_valid_url(url: str) -> bool:
   
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


class URLShortener:
    def __init__(self):
        # Ensure database and table exist
        init_db()

        # In-memory cache: short_code -> original_url
        self.cache = {}

    def _get_next_id(self) -> int:
        """
        Generates the next numeric ID.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM urls")
        count = cursor.fetchone()[0]

        conn.close()
        return count + 1

    def shorten(self, original_url: str) -> str:
        """
        Creates or returns a short code for a URL.
        """
        original_url = normalize_url(original_url)

        if not is_valid_url(original_url):
            raise ValueError("Invalid URL")

        conn = get_connection()
        cursor = conn.cursor()

        # Check if URL already exists
        cursor.execute(
            "SELECT short_code FROM urls WHERE original_url = ?",
            (original_url,)
        )
        row = cursor.fetchone()

        if row:
            conn.close()
            return row[0]

        # Generate new short code
        short_code = encode_base62(self._get_next_id())

        cursor.execute(
            """
            INSERT INTO urls (short_code, original_url, clicks, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (short_code, original_url, 0, datetime.utcnow().isoformat())
        )

        conn.commit()
        conn.close()

        return short_code

    def expand(self, short_code: str):
        """
        Returns the original URL and increments click count.
        Uses cache-aside strategy.
        """
        # 1️⃣ Cache hit
        if short_code in self.cache:
            original_url = self.cache[short_code]

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
                (short_code,)
            )
            conn.commit()
            conn.close()

            return original_url

        # 2️⃣ Cache miss → DB lookup
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT original_url FROM urls WHERE short_code = ?",
            (short_code,)
        )
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        original_url = row[0]

        # Increment clicks
        cursor.execute(
            "UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
            (short_code,)
        )

        conn.commit()
        conn.close()

        # 3️⃣ Store in cache
        self.cache[short_code] = original_url

        return original_url

    def get_stats(self, short_code: str):
        """
        Returns analytics for a short URL.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT original_url, clicks, created_at
            FROM urls
            WHERE short_code = ?
            """,
            (short_code,)
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        original_url, clicks, created_at = row

        return {
            "short_code": short_code,
            "original_url": original_url,
            "clicks": clicks,
            "created_at": created_at
        }
