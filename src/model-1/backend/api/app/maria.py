import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import *

from datetime import datetime

from sqlalchemy import create_engine, text


class Maria :

    def __init__(self) -> None:
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)


    def create_item(self, id_code, brand,name,ingredient,allergen,nutriment,nutriscore,ecoscore,packaging,image,url_openfoodfact):
        with self.engine.connect() as connection:
            query = text("INSERT INTO items (id_code, brand,name,ingredient,allergen,nutriment,nutriscore,ecoscore,packaging,image,url_openfoodfact) VALUES (:id_code, :brand, :name, :ingredient, :allergen, :nutriment, :nutriscore, :ecoscore, :packaging, :image, :url_openfoodfact)")
            connection.execute(query, id_code=id_code, brand=brand,name=name,ingredient=ingredient,allergen=allergen,nutriment=nutriment,nutriscore=nutriscore,ecoscore=ecoscore,packaging=packaging,image=image,url_openfoodfact=url_openfoodfact) 

    def update_item(self, item_id, new_name, new_description):
        with self.engine.connect() as connection:
            query = text("UPDATE items SET name=:new_name, description=:new_description WHERE id=:item_id")
            connection.execute(query, new_name=new_name, new_description=new_description, item_id=item_id)

    def delete_item(self, item_id):
        with self.engine.connect() as connection:
            query = text("DELETE FROM items WHERE id=:item_id")
            connection.execute(query, item_id=item_id)




    def create_user(self, id_code, brand,name,ingredient,allergen,nutriment,nutriscore,ecoscore,packaging,image,url_openfoodfact):
        with self.engine.connect() as connection:
            query = text("INSERT INTO items (id_code, brand,name,ingredient,allergen,nutriment,nutriscore,ecoscore,packaging,image,url_openfoodfact) VALUES (:id_code, :brand, :name, :ingredient, :allergen, :nutriment, :nutriscore, :ecoscore, :packaging, :image, :url_openfoodfact)")
            connection.execute(query, id_code=id_code, brand=brand,name=name,ingredient=ingredient,allergen=allergen,nutriment=nutriment,nutriscore=nutriscore,ecoscore=ecoscore,packaging=packaging,image=image,url_openfoodfact=url_openfoodfact)

    def update_user(self, item_id, new_name, new_description):
        with self.engine.connect() as connection:
            query = text("UPDATE items SET name=:new_name, description=:new_description WHERE id=:item_id")
            connection.execute(query, new_name=new_name, new_description=new_description, item_id=item_id)

    def delete_user(self, item_id):
        with self.engine.connect() as connection:
            query = text("DELETE FROM items WHERE id=:item_id")
            connection.execute(query, item_id=item_id)
