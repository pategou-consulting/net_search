import requests
from bs4 import BeautifulSoup
import os

# création du path pour la sauvegarde des images
def create_dir(path:str)->None:
    """ path : Chemin d'accès du dossier où seront stocker les images télécharger  """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
            print("Création du path réussi")
    except OSError:
        print("Error")


# cette fonction permet de télécharger une image 
def save_imag(url_image:str, 
              name:str)->None:
    """
    url_image: url de l'image à télécharger 
    name: nom qu'on attribue a l'image
    """
    create_dir("data/images_folder")
    # Envoyer une requête GET à l'URL
    image_response = requests.get(url_image)

    # Vérifier le code de status de la requête
    if image_response.status_code == 200:

        # Enregistrer l'image sur le disque
        with open("data/images_folder/"+name+".png", "wb") as f:
            f.write(image_response.content)

        # Afficher un message de réussite
        print("L'image a été téléchargée avec succès !")

    else:
        print(f"Échec du téléchargement de l'image : {image_response.status_code}")




# fonction pour extraire la description
def extract_product_description(url:str):
    # Faites une requête pour obtenir le contenu de la page web
    response = requests.get(url)
    
    # Vérifiez si la requête a réussi
    if response.status_code == 200:
        # Utilisez BeautifulSoup pour analyser le contenu de la page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Recherchez les balises qui contiennent les informations sur la description du produit
        descriptions = []
        possible_tags = ['p', 'div', 'span', 'li']  # Ajoutez d'autres balises possibles si nécessaire
        
        for tag in possible_tags:
            descriptions.extend([p.get_text() for p in soup.find_all(tag)])
        
        return descriptions
    else:
        return None

# # Exemple d'utilisation : remplacez l'URL par celle du site à partir duquel vous souhaitez extraire les descriptions
# url="https://www.microlinksa.com/paoduit/hp-deskjet-2630-imprimante-multifonction/"
# descriptions = extract_product_description(url)

# sauvegarder la description
# def save_desc_product(desc:str)->None:
#     with open()


# if descriptions:
#     for desc in descriptions:
#         print(desc)
# else:
#     print("Erreur lors de la récupération des descriptions du produit.")