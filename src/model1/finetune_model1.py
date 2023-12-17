import sys
import os

import mlflow


# Création du dataset
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print(sys.path)

from ultralytics import YOLO

# mlflow.autolog() 

# Load a COCO-pretrained YOLOv8n model
model = YOLO('../../checkpoints/yolov8n.pt')

hyperparameters = {"epochs" : 100,
                   "imgsz" : 640}

results = model.train(data='src/model1/dataset_custom_object.yaml', **hyperparameters)


# Set our tracking server uri for logging
# mlflow.set_tracking_uri(uri="http://127.0.0.1:8080")

# # Create a new MLflow Experiment
# mlflow.set_experiment("MLflow Quickstart")

# Start an MLflow run
# with mlflow.start_run():
#     # Log the hyperparameters
#     mlflow.log_params(hyperparameters)

#     # Log the loss metric
#     # mlflow.log_metric("accuracy", accuracy)

#     # Set a tag that we can use to remind ourselves what this run was for
#     mlflow.set_tag("Training Info", "Model détection aritcle")

#     # Log the model
#     model_info = mlflow.pytorch.log_model(
#         model, 
#         "yolo",
#     )

# # import fiftyone as fo
# # import fiftyone.zoo as foz

# # # Télécharger le dataset open image 

# # if len(os.listdir(os.path.join("src","model1","datasets","open_image"))) == 0 :

# #     # Charger le dataset Open Images

# #     dataset = foz.load_zoo_dataset("open-images-v7")

# #     # Filtrer les annotations pour les classes spécifiques
# #     filtered_view = dataset.filter_labels(
# #         "ground_truth",
# #         [{"$in": ["Box", "Bottle", "Tin can"]}],
# #         only_matches=True,
# #     )

# #     # Exporter le sous-ensemble filtré
# #     filtered_dataset = fo.Dataset.from_iterator(filtered_view)
# #     filtered_dataset.export(
# #         os.path.join("src","model1","datasets","open_image"),
# #         dataset_type=fo.types.COCODetectionDataset,
# #     )

