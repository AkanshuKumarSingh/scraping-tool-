"""
Main module containing endpoints for performing actions
"""

from fastapi import FastAPI, Depends, HTTPException, Header


from Scraper import Scraper
from model import RequestModel

app = FastAPI()

SECRET_TOKEN = "ABC1234ACB"

def authenticate(authorization: str = Header(...)):
    """
    Basic authentication to check if the token is valid.
    """
    if authorization != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return authorization

@app.post("/scrape-products")
def scrape(request_data: RequestModel, authorization: str = Depends(authenticate)):
    """
    Endpoint to scrape the data from website using the passed request data.
    """
    
    scraper = Scraper(request_data)
    scraper.start()
    return {"status": "Scraping completed", "products_scraped": len(scraper.product_selected)}
