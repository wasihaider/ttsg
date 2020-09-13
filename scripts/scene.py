from nltk import sent_tokenize
from scripts.mongo_connection import db_images
from scripts.Image_Generation import MainImage, ObjectImage
from scripts.tree import GenerateTree
from scripts.Sentence_Parsing import SentenceParser
from scripts.constants_ttsg import RELATIONS, MAIN_IMAGE_RELATIONS, IMAGES_DIR, WORK_DIR
from io import BytesIO
import base64


class Scene:
	def __init__(self):
		self.tree = GenerateTree()
		self.scene = MainImage()
		self.objects = []

	def add_node_to_tree(self, objects):
		parent = objects.get('parent')
		child = objects.get('child')
		it = objects.get('case_it')
		relation = objects.get('relation')

		if parent is None:
			self.tree.add_node(parent, child, relation)
			return
		elif it:
			recent_object = self.tree.recentObject
			if parent.name == 'it':
				self.tree.add_node(recent_object, child, relation)
			else:
				self.tree.add_node(parent, recent_object, relation)
			return
		elif parent.determiner and parent.determiner.lower() == "the":
			recent_parent = self.tree.recentParent.get(parent.name)
			if recent_parent is None:
				self.tree.add_node(parent, child, relation)
			else:
				self.tree.add_node(recent_parent, child, relation)
		else:
			self.tree.add_node(parent, child, relation)

	def add_images_to_scene(self, img):
		collection = db_images['default_image']
		print(type(img))
		for root in self.tree.roots:
			try:
				self.objects.append(root.name.title())
				# path = "".join([IMAGES_DIR, root.name, ".png"])
				if img and root.name.title() in img.keys():
					image_data = db_images['image'].find_one({'name': img[root.name.title()]}, {'_id': 0})
					b64 = image_data['image']
					buf = BytesIO(base64.b64decode(b64))
					image = ObjectImage(buf)
					size = collection.find_one({'name': root.name}, {'_id': 0})
					image.resize(size['size'])
				else:
					image_data = collection.find_one({'name': root.name}, {'_id': 0})
					b64 = image_data['image']
					buf = BytesIO(base64.b64decode(b64))
					image = ObjectImage(buf)
				if root.adjectives:
					prop = None
					for adj in root.adjectives:
						if adj == "big" or adj == "small":
							prop = adj
							break

					if prop:
						if prop == "big":
							x, y = image.size
							image.resize((x*2, y*2))
						else:
							x, y = image.size
							image.resize((x / 2, y / 2))
				print("Adding {} to scene".format(root.name))
				if root.relation_to_parent not in MAIN_IMAGE_RELATIONS:
					dims = self.scene.add_object(image, 'center')
				else:
					dims = self.scene.add_object(image, root.relation_to_parent)
				print("added on ", dims)
				image.start = dims.get('start')
				image.end = dims.get('end')
				root.image = image
				print("added on {}-{} ".format(root.image.start, root.image.end))
				self.add_images_to_root(root, img)
			except Exception as e:
				print("Exception in add_image_to_scene: ", str(e))
				continue

	def add_images_to_root(self, root, img):
		if root.children is None:
			return
		collection = db_images['default_image']
		for child in root.children:
			try:
				# path = "".join([IMAGES_DIR, child.name, ".png"])
				self.objects.append(child.name.title())
				if img and child.name.title() in img.keys():
					image_data = db_images['image'].find_one({'name': img[child.name.title()]}, {'_id': 0})
					b64 = image_data['image']
					buf = BytesIO(base64.b64decode(b64))
					image = ObjectImage(buf)
					size = collection.find_one({'name': child.name}, {'_id': 0, 'size': 1})
					image.resize(size['size'])
				else:
					print("Object: ", child.name)
					image_data = collection.find_one({'name': child.name}, {'_id': 0})
					b64 = image_data['image']
					buf = BytesIO(base64.b64decode(b64))
					image = ObjectImage(buf)
				print("Adding {} to scene".format(child.name))
				self.objects.append(child.name.title())
				if child.relation_to_parent not in RELATIONS:
					dims = self.scene.add_object_to(root.image, image, 'center')
				else:
					if image == 'jug' and child.relation_to_parent == 'center':
						dims = self.scene.add_object_to(root.image, image, child.relation_to_parent, sub_y = 180)
					else:
						dims = self.scene.add_object_to(root.image, image, child.relation_to_parent)

				image.start = dims.get('start')
				image.end = dims.get('end')
				child.image = image
				print("added on {}-{} ".format(child.image.start, child.image.end))

				for child in root.children:
					self.add_images_to_root(child, img)

			except Exception as e:
				print("Exception in add_image_to_root: ", str(e))
				continue

	def parse_text_and_generate_tree(self, text):
		try:
			sentences = sent_tokenize(text)
			for sentence in sentences:
				parser = SentenceParser(sentence)
				objects = parser.objects_with_relation()
				self.add_node_to_tree(objects)

			self.tree.print_tree()
		except Exception as e:
			print("Excecption in parse_text_and_generate_tree: ", str(e))

	def generate_scene(self, text, image = None):
		if image is None:
			image = {}
		try:
			self.parse_text_and_generate_tree(text)
			self.add_images_to_scene(image)
			b64_string = self.scene.save_image()
			data = {
				'scene': b64_string,
				'objects': list(set(self.objects))
			}
			return data
		except Exception as e:
			print("Exception in scene.py (generate_scene method)", str(e))


if __name__ == '__main__':
	paragraph = """There was a table in the Room"""

	scene = Scene()
	scene.parse_text_and_generate_tree(paragraph)
	scene.add_images_to_scene()
	scene.scene.img.show()
