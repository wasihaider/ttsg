from PIL import Image
from io import BytesIO
import base64
from mongo_connection import db_images


def get_base64_encoded_image(image_path):
	with open(image_path, "rb") as img_file:
		return base64.b64encode(img_file.read()).decode('utf-8')


if __name__ == "__main__":
	name = "bottle"
	path = "/home/heartfalcon/PycharmProjects/ttsg/flask_ttsg/static/images/{}.png".format((name))
	print(path)
	data = get_base64_encoded_image(path)
	buf = BytesIO(base64.b64decode(data))
	image = Image.open(buf)
	size = image.size
	collection = db_images['default_image']
	collection.update({'name': name}, {'$set': {'size': size, 'image': data}}, upsert = True)
