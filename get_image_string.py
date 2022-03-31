import base64

with open("./skull_icon.png", "rb") as image_file:
    image_data_base64_encoded_string = base64.b64encode(image_file.read())

print(image_data_base64_encoded_string)