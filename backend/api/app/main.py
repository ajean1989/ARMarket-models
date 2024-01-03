import json

from fastapi import FastAPI, HTTPException, UploadFile, File, Query, Form
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Annotated
from app import mongo
from app import maria


app = FastAPI()

mg = mongo.Mongo()
mr = maria.Maria()


@app.get("/")
def read_root():
    return {"Hello": "World"}




# Interact with Mongo DB

@app.get("/dataset/{id}")
def get_dataset(id: int):

    zip_path = mg.get_dataset_id(id)

    if zip_path == False :
        raise HTTPException(status_code=400, detail="ID inexistant ou vide")

    try:
        return FileResponse(zip_path, media_type="application/zip", filename=f"dataset_{id}.zip")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier ZIP non trouvé")

class Detection(BaseModel):
    label: str
    label_int: int
    bounding_box: list

class training_data(BaseModel):
    objets: List[Detection]

@app.post("/dataset/frame/")
def add_frame(image: list[UploadFile]):
    if not image[0].filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return JSONResponse(content={"error": "L'image doit avoir une extension .png, .jpg ou .jpeg"}, status_code=405)
   
    metadata = eval(image[2].file.read().decode("utf-8"))

    mg.set_img(image[0].file.read(), image[1].file.read(), dataset_id = metadata["dataset_id"], dataset_extraction = metadata["dataset_extraction"], pretreatment = metadata["pretreatment"], data_augmentation = metadata["data_augmentation"], test = metadata["test"])
    
    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)


@app.put("/dataset/frame/{id}")
def add_frame(image: UploadFile = File(...), txt: UploadFile = File(...)):
    if not image.filename.lower().endswith((".png", ".jpg", ".jpeg")):
        return JSONResponse(content={"error": "L'image doit avoir une extension .png, .jpg ou .jpeg"}, status_code=405)

    if not txt.filename.lower().endswith(".txt"):
        return JSONResponse(content={"error": "Le fichier texte doit avoir une extension .txt"}, status_code=405)
    
    # possible de rajouter dataset id / data augmentation / test à set_img
    mg.set_img(image, txt)
    
    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)
    

@app.delete("/dataset/frame/{id}")
def delete_frame(id: int):
    mg.delete_frame(id)
    try:
        return JSONResponse(content={"message": "Élément supprimé avec succès"}, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="ID inexistant")



# Interact with Maria DB

@app.get("/datawarehouse")
def delete_data(idUser: Optional[int] = None, idItem: Optional[int] = None, idPlace: Optional[int] = None):
    # Logique pour effectuer une requête SQL dans le data warehouse
    return {"message": "Data deleted successfully"}


@app.delete("/datawarehouse")
def delete_data(idUser: Optional[int] = None, idItem: Optional[int] = None, idPlace: Optional[int] = None):
    # Logique pour effectuer une requête SQL dans le data warehouse
    return {"message": "Data deleted successfully"}


@app.post("/datawarehouse/item")
def record_scan(item: dict):
    
    id_code = item["code"]
    name = item["abbreviated_product_name_fr"]
    brand = item["brand"]
    ingredient = item["ingredient"]
    allergen = item["allergen"]
    nutriment = item["nutriment"]
    nutriscore = item["nutriscore"]
    ecoscore = item["ecoscore"]
    packaging = item["packaging"]
    image = item["image"]
    url_openfoodfact = item["url_off"]
    mr.create_item(id_code=id_code, name=name, brand=brand, ingredient=ingredient, allergen=allergen, nutriment=nutriment, nutriscore=nutriscore, ecoscore=ecoscore , packaging=packaging, image=image, url_openfoodfact=url_openfoodfact)

    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)

@app.post("/datawarehouse/user")
def record_user(user: dict):
    
    username = user["username"]
    age = user["age"]
    gender = user["age"]
    mr.create_user(username=username, age=age, gender=gender)

    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)

@app.post("/datawarehouse/scan")
def record_scan(scan_data: dict):
    
    name = scan_data["abbreviated_product_name_fr"]
    # To Continue
    mr.create_item(name=name)

    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)


