# Installation

python 3.11
requirements.txt

# Branches

+ master 
+ dev 
+ test (feature unit test)

# Dossiers

## Checkpoint dans gitignore 

télécharger les modèles yolov8x et yolov8x 
https://github.com/ultralytics/ultralytics/tree/main
On peut télécharger les checkpoints pour COCO ou openimageV7, détection ou segmentation. 

## Data
### Sample

Dans git. Il y a quelques exemples de données pour faire des tests.

### Dataset dans gitignore

On peut ajouter d'autre dataset dans gitignore pour l'entrainement des modèles.

## Modeles

### Modele 1 (Projet E1)


Modèle de détection d'objet (actuellement yolov8 pré-entrainé). Il est utilisé pour la création automatique du dataset.
A terme, il faudra améliorer le modèle pour qu'il se spécialise dans la reconnaissance des articles de magasin. 

### Modele 2 

Modèle qui servira à associer une image à un code barre. 

## Backend

Script d'anotation automatique.

### API

Mise en place de l'API sur un VPS.

### MariaDB

Initialisation du modèle de données de la base MariaDB. 

## Trackers

Configuration des trackers utilisés avec YoloV8