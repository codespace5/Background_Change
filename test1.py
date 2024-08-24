
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
import ftplib
from flask import render_template, request, jsonify

from datetime import datetime    
foreground = Image.open("input.png").convert("RGBA")
background = Image.open('background1.jpg').convert("RGBA")

# Resize the background to match the size of the foreground
background = background.resize(foreground.size, Image.Resampling.LANCZOS)

# Composite the images
combined = Image.alpha_composite(background, foreground)

# Composite the images
combined = Image.alpha_composite(background, foreground)
# result_path = "./src/static/results/output123.png"
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
# result_path = f"./output_{timestamp}.png"
result_path = f"./outputo.png"
combined.save(result_path)
img = cv2.imread("1.jpeg")
cv2.imshow("result", img)
cv2.waitkey(0)
print("completed")


base_prompt = "Realistic images, high quality, high resolution, 4K, 8K, 16K, 64K"