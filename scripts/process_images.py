from scripts.mongo_connection import db_images
from flask import abort
from scripts.scene import Scene
import json


###########################################################

def process_get_images(body):
	try:
		if "category" not in body or "type" not in body:
			return json.dumps({'message': "BAD REQUEST"}), 400, {"ContentType": "application/json"}
		collection = db_images['image']
		if body['type'] == "all":
			cats = collection.distinct('category')
			data = collection.find({}, {'_id': 0})
			return json.dumps({'categories': cats, 'images': list(data)}), 200, {"ContentType": "application/json"}
		else:
			data = collection.find({'category': body['category']}, {'_id': 0})
			return json.dumps(list(data)), 200, {"ContentType": "application/json"}
	except Exception as e:
		print("Exception in process_get_images: ", str(e))
		abort(503)


###########################################################

def process_delete_image(body):
	try:
		if 'name' not in body:
			return json.dumps({'message': "BAD REQUEST"}), 400, {"ContentType": "application/json"}
		collection = db_images['image']
		data = collection.remove({'name': body['name']})
		return json.dumps({'message': "SUCCESS"}), 200, {"ContentType": "application/json"}
	except Exception as e:
		print("Exception in process_delete_image: ", str(e))
		abort(503)


###########################################################

def process_add_image(body):
	try:
		print(1)
		if "category" not in body and "image" not in body:
			return json.dumps({'message': "BAD REQUEST"}), 400, {"ContentType": "application/json"}
		collection = db_images['image']
		print(2)
		print(body)
		cur_nam_val = db_images['image_names'].find_one({'category': body['category']}, {'_id': 0})
		print(cur_nam_val)
		print(3)
		name = body['category'] + str(cur_nam_val['val'])
		print(4)
		collection.insert({'name': name, 'image': body['image'], 'category': body['category']})
		db_images['image_names'].update({'category': body['category']}, {'$inc': {'val': 1}})
		print(5)
		return json.dumps({'message': "SUCCESS"}), 200, {"ContentType": "application/json"}
	except Exception as e:
		print("Exception in process_add_image: ", str(e))
		abort(503)


###########################################################

def process_generate_image(body):
	try:
		if "type" not in body:
			return json.dumps({"messgae": "BAD REQUEST"}), 400, {"Content-Type": "application/json"}
		if body['type'] == "new":
			if "input" not in body:
				return json.dumps({"messgae": "BAD REQUEST"}), 400, {"Content-Type": "application/json"}
			image = Scene()
			generated_scene = image.generate_scene(body['input'])
			return json.dumps(generated_scene), 200, {"Content-Type": "application/json"}
		elif body['type'] == "edit":
			if "input" not in body and "object" not in body:
				return json.dumps({"messgae": "BAD REQUEST"}), 400, {"Content-Type": "application/json"}
			print(body)
			image = Scene()
			generated_scene = image.generate_scene(body['input'], body['object'])
			return json.dumps(generated_scene), 200, {"Content-Type": "application/json"}
		else:
			return json.dumps({"messgae": "BAD REQUEST"}), 400, {"Content-Type": "application/json"}
	except Exception as e:
		print("Exception in process_generate_image: ", str(e))

###########################################################
