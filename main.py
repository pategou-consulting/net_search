from tools import*
from fastapi import FastAPI
from fastapi.responses import UJSONResponse
import os
import http.client
import json
import pendulum 
from dotenv import load_dotenv




load_dotenv()

app = FastAPI()

@app.post("/search/{word}",response_class=UJSONResponse)
async def search(word:str)->json:

    """
    Cette fonction est la fonction principale de l'API qui recupere en paramètre le l'article rechercher
    , (word) et renvoi un objet json de 5 éléments , constituer du:
    
     -name: nom de l'article, il est récupérer directement l'entré utilisateur,
     -title: titre de l'article,
     -price: prix de l'article,
     -image: nom reformater de l'image l'article télécharger,
     -link:  lien du site où l'article a été retrouver,
    """
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    "q": word,
    "location": "Cameroon",
    "gl": "cm",
    "hl": "fr",
    "engine": "google",
    "type": "shopping",
    "num":5
    })
    headers = {
    'X-API-KEY':os.getenv("SERPER_API_KEY"),
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/shopping", payload, headers)
    res = conn.getresponse()

    data = res.read().decode("utf-8")
    result=json.loads(data)
    

    #récupération des 5 premiers éléments
    shopping_results=result["shopping"][:5]
    response=[]
    for elt in shopping_results:

        title= elt["title"]
        price=elt["price"]
        date_heure = pendulum.now("Africa/Douala")
        image_name = f"image_{date_heure.strftime('%Y-%m-%d_%H-%M-%S')}.png"
        image_url=elt["imageUrl"]
        link=elt["link"]
        save_imag(url_image=image_url,name=image_name)
        
        data={
            "name":word,
            "title":title,
            "price":price,
            "image":image_name,
            "link":link,
        }
        
        response.append(data)

    return response








