from __future__ import print_function
from google.cloud import vision
# from google.cloud.vision import types
# import io
# from pdf2image import convert_from_path
import os, io
import pandas as pd
from gcloudparser import GcloudParser

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'gcloudkey.json'
print("hello")
# PATH = '../../grive/Belege/Gescannt_20200208-1357.pdf'
# pages = convert_from_path(PATH, 501)
# client = vision.ImageAnnotatorClient()

FILE_NAME = '1234.jpg'
FOLDER_PATH = r'/Users/jianwei/Pictures'

client = vision.ImageAnnotatorClient()
with io.open(os.path.join(FOLDER_PATH,FILE_NAME), 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content = content)
response = client.text_detection(image=image)

# client = vision.ImageAnnotatorClient()
# image = vision.Image()
# image.source.image_uri = image_uri

# response = client.text_detection(image=image)
# print(response)
# df = pd.DataFrame(columns=['locale','description'])
# for 

parser = GcloudParser(debug=False)
articles, dates, markets = parser.parse_response(response)
for artcile in articles:
    print(artcile)

# for text in response.text_annotations:
#     print('=' * 30)
#     print(text.description)
#     vertices = ['(%s,%s)' % (v.x, v.y) for v in text.bounding_poly.vertices]
#     print('bounds:', ",".join(vertices))


