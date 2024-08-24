
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
from datetime import datetime
import os

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
def backremove():
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

    url = "https://0427e94fd628580094.gradio.live"

    # Read Image in RGB order
    img = cv2.imread('output.png')

    base_prompt = "background, realistic images, high quality, high resolution, 4K, 8K, 16K, 64K"
    if not content:
        content = "forest background"
    payload = {
    "prompt": content + base_prompt,
    "negative_prompt": "wrong image, bad image",
    "batch_size": 1,
    "steps": 20,
    "cfg_scale": 7,
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    # Read and decode the response
    response_json = response.json()
    result = response_json['images'][0]
    background_image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
    background_image.save('output123.png')
    print('Background image generated')

    # Open the images using PIL
    foreground = Image.open(output_path).convert("RGBA")
    background = Image.open('output123.png').convert("RGBA")

    # Resize the background to match the size of the foreground
    background = background.resize(foreground.size, Image.Resampling.LANCZOS)

    # Composite the images
    combined = Image.alpha_composite(background, foreground)

    # Composite the images
    combined = Image.alpha_composite(background, foreground)
    # result_path = "./src/static/results/output123.png"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    result_path = f"./src/static/results/output_{timestamp}.png"
    combined.save(result_path)
    
    print("completed")
    return jsonify({"path": "http://34.148.69.171:5000/" + result_path[6:]})


@app.route("/backchange", methods=["POST", "GET"])
def backchange():
    req_data = request.get_json()
    image_data = req_data["image"]
    background = req_data["background"]
    content = req_data["text"]
    
    # Decode base64 image data
    image_data_decoded = base64.b64decode(image_data.split(",")[1])
    background_decoded = base64.b64decode(background.split(",")[1])
    # Save the image to a file
    image_path = "image.jpg"
    background_path = "background.png"
    with open(image_path, "wb") as img_file:
        img_file.write(image_data_decoded)
    with open(background_path, "wb") as bk_file:
        bk_file.write(background_decoded)

    input_path = 'image.jpg'
    output_path = 'output.png'

    input = cv2.imread(input_path)
    output = remove(input)
    cv2.imwrite(output_path, output)

    # Open the images using PIL
    foreground = Image.open("output.png").convert("RGBA")
    background = Image.open('background.png').convert("RGBA")

    # Resize the background to match the size of the foreground
    background = background.resize(foreground.size, Image.Resampling.LANCZOS)

    # Composite the images
    combined = Image.alpha_composite(background, foreground)

    # Composite the images
    combined = Image.alpha_composite(background, foreground)
    # result_path = "./src/static/results/output123.png"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    result_path = f"./src/static/results/output_{timestamp}.png"
    combined.save(result_path)
    
    print("completed")
    return jsonify({"path": "http://34.148.69.171:5000/" + result_path[6:]})


@app.route("/removeback", methods=["POST", "GET"])
def backchange():
    req_data = request.get_json()
    image_data = req_data["image"]
    background = req_data["background"]
    content = req_data["text"]
    
    # Decode base64 image data
    image_data_decoded = base64.b64decode(image_data.split(",")[1])
    background_decoded = base64.b64decode(background.split(",")[1])
    # Save the image to a file
    image_path = "image.jpg"
    background_path = "background.png"
    with open(image_path, "wb") as img_file:
        img_file.write(image_data_decoded)
    with open(background_path, "wb") as bk_file:
        bk_file.write(background_decoded)

    input_path = 'image.jpg'
    output_path = 'output.png'

    input = cv2.imread(input_path)
    output = remove(input)
    cv2.imwrite(output_path, output)

    # Open the images using PIL
    foreground = Image.open("output.png").convert("RGBA")
    background = Image.open('background.png').convert("RGBA")

    # Resize the background to match the size of the foreground
    background = background.resize(foreground.size, Image.Resampling.LANCZOS)

    # Composite the images
    combined = Image.alpha_composite(background, foreground)

    # Composite the images
    combined = Image.alpha_composite(background, foreground)
    # result_path = "./src/static/results/output123.png"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    result_path = f"./src/static/results/output_{timestamp}.png"
    combined.save(result_path)
    
    print("completed")
    return jsonify({"path": "http://34.148.69.171:5000/" + result_path[6:]})



    # if os.path.exists(image_path):
    #     os.remove(image_path)
    # if os.path.exists(output_path):
    #     os.remove(output_path)
    # if os.path.exists('output123.png'):
    #     os.remove('output123.png')


    # if os.path.exists(image_path):
    #     os.remove(image_path)
    # if os.path.exists(background_path):
    #     os.remove(background_path)
    # if os.path.exists(output_path):
    #     os.remove(output_path)