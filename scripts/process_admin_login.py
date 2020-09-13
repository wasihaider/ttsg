from scripts.mongo_connection import db_users
from flask import abort
import json


###########################################################

def process_admin_login(body):
	print("USER REQUEST: ", body)
	if 'username' not in body or 'password' not in body:
		return json.dumps({"message": "BAD REQUEST"}), 400, {"ContentType": "application/json"}
	user_data = db_users['users'].find_one({'username': body['username']}, {'_id': 0})
	if user_data:
		if body['password'] == user_data['password']:
			return json.dumps({"message": "SUCCESS"}), 200, {"ContentType": "application/json"}
		else:
			return json.dumps({"message": "INVALID PASSWORD"}), 401, {"ContentType": "application/json"}
	else:
		return json.dumps({"message": "INVALID USERNAME"}), 401, {"ContentType": "application/json"}


###########################################################
