from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
from collections import Counter
from ultralytics import YOLO
import base64
from io import BytesIO
from PIL import Image


app = Flask(__name__)
api = Api(app)

model = YOLO('data/yolov8_food.pt')
food_by_ingredients = pd.read_json('data/food_by_ingredients.json', orient='columns').set_index('ingredients')
with open('data/detection-model-class-id-encode.txt', 'r') as f:
    id_mapping = [int(w) for w in f.read().split()]


class Recommender(Resource):
    def post(self):
        list_of_ingredients = request.get_json(True)['ingredient_ids']
        return {
            'food_ids': [idx for idx,_ in Counter(food_by_ingredients.loc[list_of_ingredients, 'id'].sum()).most_common(20)]
        }


class Detector(Resource):
    def post(self):
        datarequest = request.get_data()
        image_data = base64.b64decode(datarequest)
        img = Image.open(BytesIO(image_data))
        out = model.predict(img, iou=0.5, imgsz=320, conf=0.3)[0]
        cls = out.boxes.cls.numpy()
        xywh = out.boxes.xywh.numpy()
        results = []

        for c, d in zip(cls, xywh):
            results.append({"ingredient_id" : id_mapping[int(c)],
                            "box":d.tolist()})    
        return results


api.add_resource(Recommender, "/recommend")
api.add_resource(Detector, "/detect/")

app.run()
