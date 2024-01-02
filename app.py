from flask import Flask, request
from flask_restful import Resource, Api
import pandas as pd
from collections import Counter
from ultralytics import YOLO
import base64
from io import BytesIO
from PIL import Image
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

model = YOLO('data/yolov8_food.pt')
food_by_ingredients = pd.read_json(
    'data/food_by_ingredients.json', orient='columns').set_index('ingredients')
with open('data/detection-model-class-id-encode.txt', 'r') as f:
    id_mapping = [int(w) for w in f.read().split()]


class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello, World!'}


class Recommender(Resource):
    def post(self):
        list_of_ingredients = request.get_json(True)['ingredient_ids']
        return {
            'food_ids': [idx for idx, _ in Counter(food_by_ingredients.loc[list_of_ingredients, 'id'].sum()).most_common(20)]
        }


class Detector(Resource):

    @staticmethod
    def PIL_to_base64_str(img: Image):
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def post(self):
        datarequest = request.get_json()['image']
        image_data = base64.b64decode(datarequest)
        img = Image.open(BytesIO(image_data))
        out = model.predict(img, iou=0.5, imgsz=320, conf=0.3)[0]
        predicted_img = Image.fromarray(out.plot()[..., ::-1]).resize(size=(415, 360))
        cls = out.boxes.cls.numpy()
        xyxy = out.boxes.xyxy.numpy()
        results = [{"ingredient_id": -1,
                    "image": self.PIL_to_base64_str(predicted_img)}]

        for c, d in zip(cls, xyxy):
            results.append({"ingredient_id": id_mapping[int(c)],
                            "image": self.PIL_to_base64_str(img.crop(d).resize(size=(60, 60)))})
        return results


api.add_resource(HelloWorld, "/")
api.add_resource(Recommender, "/recommend")
api.add_resource(Detector, "/detect/")

if __name__ == "__main__":
    app.run(port=8080)
