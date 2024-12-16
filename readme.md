# Scraper Application

## Overview
This project is a web scraping application built using **FastAPI** and **Redis**. The application scrapes product data from a specified e-commerce website and caches the data using Redis to avoid redundant processing. It also supports basic token-based authentication for secure access to its endpoints.

---

## Features
- **Token-based Authentication**: Ensures only authorized users can access the scraping endpoint.
- **Redis Integration**: Caches product data to optimize performance and prevent redundant processing.
- **Image Processing**: Downloads and saves product images locally.
- **Retry Mechanism**: Handles transient errors by retrying failed requests.
- **JSON Export**: Saves the scraped product data into a JSON file.

---

## Installation

### Prerequisites
- Python 3.7 or higher
- Redis server
- Pipenv or pip for dependency management

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/AkanshuKumarSingh/scraping-tool-.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Redis server:
   ```bash
   redis-server
   ```

4. Run the FastAPI application:
   ```bash
   uvicorn app:app --reload
   ```

5. Access the application at:
   [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Usage

### Authentication
The application uses token-based authentication. Include the following header in your requests:

```http
Authorization: ABC1234ACB
```

Replace `ABC1234ACB` with the actual token.

### Endpoints

#### POST `/scrape-products`
- **Description**: Scrapes product data from the website and saves it to Redis and a JSON file.
- **Request Body**:
  ```json
  {
      "proxy": "<optional_proxy_url>",
      "max_pages": 2
  }
  ```
  
  - `proxy`: (Optional) Proxy URL for making requests.
  - `max_pages`: The maximum number of pages to scrape.

- **Response**:
  ```json
  {
      "status": "Scraping completed",
      "products_scraped": <number_of_products_scraped>
  }
  ```

### Example Request (Using `curl`):
```bash
curl -X POST \
  'http://127.0.0.1:8000/scrape-products' \
  -H 'Authorization: ABC1234ACB' \
  -H 'Content-Type: application/json' \
  -d '{
    "proxy": "",
    "max_pages": 5
  }'
```

---

## Code Structure

### `main.py`
- Contains the FastAPI application and endpoint definitions.
- Implements token-based authentication via the `authenticate` function.

### `Scraper.py`
- Contains the `Scraper` class, which:
  - Fetches HTML content from the target website.
  - Parses product data (title, price, image).
  - Caches product data in Redis.
  - Downloads and saves product images locally.

### `model.py`
- Defines the `RequestModel` class for request validation.

---

## Configuration

### Environment Variables
- **SECRET_TOKEN**: The token used for authenticating API requests.

### Redis Configuration
Ensure Redis is running on `localhost` with the default port `6379`. If Redis is hosted elsewhere, update the `host` and `port` in the following line in `Scraper.py`:

```python
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
```

---

## Output
- **Product Data**: Saved to a file named `product_data.json`.
- **Images**: Stored in the `images/` directory.

---

## Error Handling
- **Authentication Errors**: Returns a `401 Unauthorized` response if the token is invalid.
- **Retry Mechanism**: Retries failed requests up to `max_retries` times with a delay of `retry_sec` seconds.
- **Redis Errors**: Logs errors if Redis is not reachable or fails to store data.

---

## Dependencies
- **FastAPI**: For building the web application.
- **Redis**: For caching product data.
- **BeautifulSoup**: For parsing HTML content.
- **Requests**: For making HTTP requests.
- **Uvicorn**: For running the FastAPI application.

Install all dependencies using:
```bash
pip install -r requirements.txt
```

---

## Acknowledgments
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/docs/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

