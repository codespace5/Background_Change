
# import ftplib
# from flask import Flask, render_template, request, jsonify
# # from werkzeug.utils import secure_filename
# import base64
# from rembg import remove
# import cv2
# import json
# import requests
# import io
# import base64
# from PIL import Image


# input_path = '2.jpeg'
# output_path = 'output.png'


# input = cv2.imread(input_path)
# output = remove(input)
# cv2.imwrite(output_path, output)

# print("background removed")
# url = "https://9115e99f2cd524c83f.gradio.live"

# # Read Image in RGB order
# img = cv2.imread('output.png')



# payload = {
# "prompt": 'forest background',
# "negative_prompt": "",
# "batch_size": 1,
# "steps": 20,
# "cfg_scale": 7,
# }

# response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

# # Read results
# r = response.json()
# result = r['images'][0]
# image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
# image.save('output123.png')

# print('complete')


import cv2
from rembg import remove
import requests
import io
import base64
from PIL import Image

# Paths for input and output images
input_path = 'model1.jpg'
output_path = 'output.png'
final_output_path = 'final_output.png'

# Remove background from the input image
input_image = cv2.imread(input_path)
output_image = remove(input_image)
cv2.imwrite(output_path, output_image)
print("Background removed")

# URL for the API
url = "https://429fe1041ce59d793d.gradio.live"

# Payload for the API request
payload = {
    "prompt": 'forest background, realistic, 16k, high resolution, realistic image, high quality',
    "negative_prompt": "bad image, wrong image",
    "batch_size": 1,
    "steps": 20,
    "cfg_scale": 7,
}

# Make the API request
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
# combined = Image.blend(foreground, background, alpha=.49)


# Save the final output
combined.save(final_output_path)
print('Images combined and saved as final_output.png')
cv2.imshow("result", combined)

cv2.waitkey(0)