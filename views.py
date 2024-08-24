
import ftplib
from flask import Flask, render_template, request, jsonify
# from werkzeug.utils import secure_filename
import base64
from rembg import remove
import cv2
import json
import requests
import io
import base64
from PIL import Image
from src.gradio_demo import SadTalker
import ftplib
from flask import render_template, request, jsonify
from src import app
from text2speech import synthesize_text
from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/home')
def home():
    ''' Renders the home page '''
    print("!Start")
    return render_template(
        "index.html"
    )

@app.route("/videogen", methods=["POST","GET"])
def videogen():
    req_data = request.get_json()
    image_data = req_data["image"]
    audio_path = req_data["audio"]
    content = req_data["text"]
    
    # Decode base64 image data
    image_data_decoded = base64.b64decode(image_data.split(",")[1])

    # Save the image to a file
    image_path = "image.jpg"
    with open(image_path, "wb") as img_file:
        img_file.write(image_data_decoded)

    text = content
    gender = "female"

    synthesize_text(gender, text, 'qqq.wav')
    sadtalker = SadTalker()
    res_path, video_name = sadtalker.test(image_path, 'qqq.wav')  
    result_path = "http://34.148.69.171:5000/" + res_path[6:]
    print("result is :", result_path)
    return jsonify({"path": result_path})

@app.route("/backremove", methods=["POST", "GET"])
def backgroundRemove():
    req_data = request.get_json()
    image_data = req_data["image"]
    audio_path = req_data["audio"]
    content = req_data["text"]
    
    # Decode base64 image data
    image_data_decoded = base64.b64decode(image_data.split(",")[1])

    # Save the image to a file
    image_path = "image.jpg"
    with open(image_path, "wb") as img_file:
        img_file.write(image_data_decoded)


    input_path = 'image.jpg'
    output_path = 'output.png'

    input = cv2.imread(input_path)
    output = remove(input)
    cv2.imwrite(output_path, output)

    url = "https://9115e99f2cd524c83f.gradio.live"

    # Read Image in RGB order
    img = cv2.imread('output.png')



    payload = {
    "prompt": 'forest background',
    "negative_prompt": "",
    "batch_size": 1,
    "steps": 20,
    "cfg_scale": 7,
}

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    # Read results
    r = response.json()
    result = r['images'][0]
    image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
    result_path = "./src/static/results/output123.png"
    image.save(result_path)

    print('complete')
    return jsonify({"path": "http://34.148.69.171:5000/" + result_path[6:]})
