# AI Services for Culinergy

### Setup
Installation dependencies
```
pip install -r requirements.txt
```
Start flask server
```
python app.py
```
Start docker:
```
sudo docker-compose up
```
### API Docs
Server Usage:

1. Ingredient Detection:

   - Method: POST
   - URL: http://127.0.0.1:5000/detect/
   - Example input: `base64` encoding of this image in key-value format.

      ![Example input image](./assets/rice_cheese_onion_ham_corn_ketchup.jpg "base64: /9j/4...5//Z")

     ```json
     { "image": "/9j/4...5//Z" }
     ```

   - Example output: `id` with `base64` encoding of cropped ingredient images. `id=-1` mean the original image with bounding box of detected ingredients.

     ```json
      [
         {
            "ingredient_id": -1,
            "image": "/9j/4...5//Z"
         },
         {
            "ingredient_id": 1789,
            "image": "/9j/4...2P/Z"
         },
         {
            "ingredient_id": 1789,
            "image": "/9j/4...2Q=="
         },
         {
            "ingredient_id": 2478,
            "image": "/9j/4...2Q=="
         }
      ]
     ```

2. Food Recommendation:

   - Method: POST
   - URL: http://127.0.0.1:5000/recommend/
   - Example input: 1789 (Cheese), 2478 (Corn)
     ```json
     { "ingredient_ids": [1789, 2478] }
     ```
   - Example output: 

     ```json
     {"food_ids": [8756, 9718, 2728, ... , 1189, 1418]}
     ```
