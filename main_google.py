from tools import*
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from serpapi import GoogleSearch
import pendulum 
from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI()
@app.get("/search/{word}")
async def search(word:str):
    params = {
        "q": word,
        "engine":"google_shopping",
        "google_domain":"google.cm",
        "hl":"fr",
        "gl":"cm",
        "num":5,
        "location":"Cameroon",
        "device":"desktop",
        "api_key": os.getenv("SERPAPI_API_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    shopping_results = results.get("shopping_results", [])
    result = {}
    response=[]
    for elt in shopping_results:

        title= elt["title"]
        price=elt["price"]
        date_heure = pendulum.now("Africa/Douala")
        image_name = f"image_{date_heure.strftime('%Y-%m-%d_%H-%M-%S')}.png"
        image_url=elt["thumbnail"]
        link=elt['link']
        save_imag(url_image=image_url,name=image_name)
        
        data={
            "name":word,
            "title":title,
            "price":price,
            "image":image_name,
            "link":link,
            "description" : extract_product_description(url=link)
        }
        
        response.append(data)
        
        
    return response

