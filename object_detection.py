import requests
import json
import cv2
import numpy as np
import os

# Load the image
image_path = "path of image"
output_dir = "Path to save the output image"
image = cv2.imread(image_path)

# Convert the image to base64 string
_, image_data = cv2.imencode('.jpg', image) 
image_base64 = image_data.tobytes()

# Sending request to BrainyPi
url = "http://127.0.0.1:9900/v1/detectobjects"  
headers = {'Content-Type': 'application/json'}
response = requests.post(url, data = image_data.tobytes())
#Save the result
def save_image(image, image_path,output_dir):
    print("Saving output image to dir {}".format(output_dir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = "result_{}".format(image_path.split('/')[-1])
    filepath = os.path.join(output_dir, filename)
    cv2.imwrite(filepath, image)

#displaying image
def display_image(image):
    cv2.imshow("Object Detection", image)
    cv2.waitKey(0)


if response.status_code == 200: 
    response_data = response.json() 
    objects = response_data["result"]["objects"]
    print(objects)

    # drawing text and boundary
    for obj in objects: 
         obj_type = obj["object"] 
         confidence = obj["confidence"]
         box = obj["boundingBox"]

         #Extracting bounding box coordinates
         top = int(box["top"])
         left = int(box["left"])
         width = int(box["width"])
         height = int(box["height"])

         # Drawing the boiunding box and type
         cv2.rectangle(image, (left, top), (left + width, top + height), (0, 255, 0), 2)
         label = f"{obj_type}: {confidence}"
         cv2.putText(image, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        #displaying image
         display_image(image)
        #Save the result
         save_image(image, image_path,output_dir)

else:
    print("Error: Request to the API server failed ", response.status_code)

