from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional
import mongo
import maria

app = FastAPI()

mg = mongo.Mongo()
mr = maria.Maria()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/dataset/{id}")
def get_dataset(id: int):

    zip_path = mg.get_dataset_id(id)

    if zip_path == False :
        raise HTTPException(status_code=400, detail="ID inexistant ou vide")

    try:
        return FileResponse(zip_path, media_type="application/zip", filename=f"dataset_{id}.zip")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Fichier ZIP non trouvé")
    
@app.delete("/dataset/{id}")
def delete_dataset(id: int):
    mg.delete_dataset_id(id)
    try:
        return JSONResponse(content={"message": "Élément supprimé avec succès"}, status_code=200)
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="ID inexistant")

@app.post("/dataset/frame")
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


@app.post("/datawarehouse/item")
def record_scan(scan_data: dict):
    
    name = scan_data["abbreviated_product_name_fr"]
    # To Continue
    mr.create_item(name=name)

    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)

@app.post("/datawarehouse/user")
def record_scan(scan_data: dict):
    
    name = scan_data["abbreviated_product_name_fr"]
    # To Continue
    mr.create_item(name=name)

    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)

@app.post("/datawarehouse/scan")
def record_scan(scan_data: dict):
    
    name = scan_data["abbreviated_product_name_fr"]
    # To Continue
    mr.create_item(name=name)

    return JSONResponse(content={"message": "Frame ajoutée avec succès"}, status_code=200)


@app.delete("/datawarehouse")
def delete_data(idUser: Optional[int] = None, idItem: Optional[int] = None, idPlace: Optional[int] = None):
    # Logique pour effectuer une requête SQL dans le data warehouse
    return {"message": "Data deleted successfully"}