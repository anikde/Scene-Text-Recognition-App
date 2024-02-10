import requests
import os

img_dir= "/home/anand/anik/dataset/DATA_CLSATR/hindi/images"
number = 209
filename = f"image_{number}.jpg"
img = os.path.join(img_dir, filename)

url = "http://10.6.0.36:8000/endtoend/"  
file = {'images': open(img, "rb")}

response = requests.post(url, files=file)
jresponse = response.json()
# print(jresponse)
sorted_response = [regions for regions in jresponse[0]["regions"]]
sorted(sorted_response, key= lambda k: k["line"], reverse=True)

print(" ".join(word["label"] for word in sorted_response))