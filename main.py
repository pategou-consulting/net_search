from fastapi import FastAPI, Depends
from fastapi.responses import UJSONResponse
from fastapi_pagination import Page, add_pagination, paginate, Params
from pydantic import BaseModel
import os
import http.client
import json
import pendulum
from dotenv import load_dotenv
from fastapi_pagination.links import Page
load_dotenv()

app = FastAPI()

class SearchItem(BaseModel):
    name: str
    title: str
    price: str
    image_url: str
    link: str

class CustomPage(Page[SearchItem]):
  

    @staticmethod
    def create(items, total, params: Params):
    
        return CustomPage(
            items=items,
            total=total,
            page=params.page,
            size=params.size,
            pages=(total + params.size - 1) // params.size,  # total number of pages
         
        )

def default_pagination_params():
    return Params( size=10)

@app.post("/search/{word}", response_model=CustomPage, response_class=UJSONResponse)
async def search(word: str, params: Params = Depends(default_pagination_params)):

    """
    Cette fonction est la fonction principale de l'API qui récupère en paramètre le mot recherché
    , (word) et renvoie un objet JSON de 5 éléments , constitué de :
    
     - name: nom de l'article, récupéré directement à partir de l'entrée utilisateur,
     - title: titre de l'article,
     - price: prix de l'article,
     - image: nom reformatté de l'image de l'article téléchargé,
     - link: lien du site où l'article a été retrouvé,
    """
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
        "q": word,
        "location": "Cameroon",
        "gl": "cm",
        "hl": "fr",
        "engine": "google",
        "type": "shopping",
        "num": 50  # fetch a larger number of items to ensure we have enough to paginate
    })
    headers = {
        'X-API-KEY': os.getenv("SERPER_API_KEY"),
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/shopping", payload, headers)
    res = conn.getresponse()

    data = res.read().decode("utf-8")
    result = json.loads(data)
    
    # Récupération des résultats de shopping
    shopping_results = result["shopping"]
    total_items = len(shopping_results)
    
    # Appliquer la pagination sur les résultats
    start_index = (params.page - 1) * params.size
    end_index = start_index + params.size
    paginated_results = shopping_results[start_index:end_index]

    # Création de la réponse paginée
    response = []
    for elt in paginated_results:
        title = elt["title"]
        price = elt["price"]
        date_heure = pendulum.now("Africa/Douala")
        image_url = elt["imageUrl"]
        link = elt["link"]
        
        data = {
            "name": word,
            "title": title,
            "price": price,
            "image_url": image_url,
            "link": link,
        }
        
        response.append(data)

    return CustomPage.create(response, total_items, params)

# Ajout de la pagination à l'application FastAPI
add_pagination(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
