from PIL import Image
from scripts.constants_ttsg import IMAGES_DIR, WORK_DIR
import base64
from io import BytesIO


#############################################################################################

class ObjectImage:
    """
    This class will contains image data for each object to be added to the whole scene
    """
    def __init__(self, path):
        self.img = Image.open(path).convert("RGBA")
        self.size = self.img.size
        self.start = ()
        self.end = ()
        self.objects_on = []

    ######################################################

    def resize(self, size):
        """
        This method is to resize the image for object
        :param size: for how much it is to be resized
        :return: returns nothing
        """
        try:
            self.img = self.img.resize(size)
            self.size = size
        except Exception as e:
            print("Exception in Image_Generation.py, Class ObjectImage (resize method)", str(e))


#############################################################################################

class MainImage:
    def __init__(self):
        self.img = Image.open("".join([IMAGES_DIR, "room.png"]))
        self.size_x, self.size_y = self.img.size
        self.added_images = []

    ######################################################

    def add_image(self, img):
        """
        This method is to add images to the list of added images on main image to keep a record
        :param img: The image object to be added to the list
        :return: returns nothing
        """
        try:
            self.added_images.append(img)
        except Exception as e:
            print("Exception in Image_Generation.py, Class MainImage (add_image method)", str(e))

    ######################################################

    def add_object(self, obj, prep, add_x = 0, add_y = 0, sub_x = 0, sub_y = 0):
        """
        This method is to add root objects on main image on the floor usually
        :param obj: The object to be added
        :param prep: The preposition e-g left, right, center
        :param add_x: optional argument to move object to right on a special case
        :param add_y: optional argument to move object downward on a special case (e-g plate on chair)
        :param sub_x: optional argument to move object left on a special case
        :param sub_y: optional argument to move object upward in a special case
        :return: returns nothing
        """
        try:
            obj_x, obj_y = obj.size
            x, y = 0, 0

            if prep == 'center':
                x = (self.size_x - obj_x) // 2 + add_x - sub_x
                y = self.size_y - obj_y - 100 + add_y - sub_y
            elif prep == 'left':
                x = 50 + add_x - sub_x
                y = self.size_y - obj_y - 100 + add_y - sub_y
            elif prep == 'right':
                x = self.size_x - obj_x - 50 + add_x - sub_x
                y = self.size_y - obj_y - 100 + add_y - sub_y

            start = (x, y)
            end = (x + obj_x, y + obj_y)
            self.img.paste(obj.img, (x, y), obj.img)
            return {'start': start, 'end': end}
        except Exception as e:
            print("Exception in Image_Generation.py, Class MainImage (add_object method)", str(e))

    ######################################################

    def add_object_to(self, obj1, obj2, prep, add_x = 0, add_y = 0, sub_x = 0, sub_y = 0):
        """
        This method is to add an object with relative to other object given
        :param obj1: Object which is parent and already on the scene
        :param obj2: Object to be added to the scene with relation to parent
        :param prep: Preposition for relation e-g left, right, on, below
        :param add_x: optional argument to move object to right on a special case
        :param add_y: optional argument to move object downward on a special case (e-g plate on chair)
        :param sub_x: optional argument to move object left on a special case
        :param sub_y: optional argument to move object upward in a special case
        :return: returns nothing
        """
        try:
            print("relation got: ", prep)
            obj1_x, obj1_y = obj1.size
            obj2_x, obj2_y = obj2.size
            x, y = 0, 0

            if prep == 'center':
                x = obj1.start[0] + ((obj1_x - obj2_x) // 2) + add_x - sub_x
                y = obj1.start[1] + add_y - sub_y
            elif prep == 'on_left':
                x = obj1.start[0] + add_x - sub_x
                y = obj1.start[1] + 10 + add_y - sub_y
            elif prep == 'on_right':
                x = obj1.end[0] - obj2_x - 50 + add_x - sub_x
                y = obj1.start[1] + 10 + add_y - sub_y
            elif prep == 'left' or prep == 'near':
                # space_on_left = obj1.start[0]
                x = obj1.start[0] - 100 - obj2_x + add_x - sub_x
                y = self.size_y - 100 - obj2_y + add_y - sub_y
            elif prep == 'below' or prep == 'under':
                x = obj1.start[0] + ((obj1_x - obj2_x) // 2) + add_x - sub_x
                y = obj1.end[1] - obj2_y + add_y - sub_y
            elif prep == "right":
                x = obj1.end[0] + 100 + add_x - sub_x
                y = self.size_y - 100 - obj2_y + add_y - sub_y
            elif prep == "far":
                x = obj1.end[0] + 300 + add_x - sub_x
                y = self.size_y - 300 - obj2_y + add_y - sub_y

            start = (x, y)
            end = (x + obj2_x, y + obj2_y)
            self.img.paste(obj2.img, (x, y), obj2.img)
            return {'start': start, 'end': end}
        except Exception as e:
            print("Exception in Image_Generation.py, Class MainImage (add_object_to method)", str(e))

    ######################################################

    def save_image(self):
        """
        This method is to save the whole scene created so far
        :return path: path of the saved image
        """
        try:
            buffered = BytesIO()
            self.img.save(buffered, format = "PNG")
            buffered.seek(0)
            img_str = str(base64.b64encode(buffered.getvalue()).decode('ascii'))
            return img_str
        except Exception as e:
            print("Exception in Image_Generation.py, Class MainImage (save_image method)", str(e))


#############################################################################################

if __name__ == '__main__':
    # main()
    sofa_path = "../Images/sofa.png"
    sofa = ObjectImage(sofa_path)

    table_path = "../Images/table.png"
    table = ObjectImage(table_path)

    plate_path = "../Images/plate.png"
    plate = ObjectImage(plate_path)

    cake_path = "../Images/cake.png"
    cake = ObjectImage(cake_path)

    pen_path = "../Images/pen.png"
    pen = ObjectImage(pen_path)

    book_path = "../Images/book.png"
    book = ObjectImage(book_path)

    chair_path = "../Images/chair.png"
    chair = ObjectImage(chair_path)

    scene = MainImage()

    dims = scene.add_object(sofa, 'center', sub_y = 200)
    sofa.start = dims.get('start')
    sofa.end = dims.get('end')
    print("sofa: ", sofa.start, sofa.end)

    dims = scene.add_object(table, 'center')
    table.start = dims.get('start')
    table.end = dims.get('end')
    print("table: ", table.start, table.end)

    dims = scene.add_object_to(table, plate, 'center')
    plate.start = dims.get('start')
    plate.end = dims.get('end')
    print("plate: ", plate.start, plate.end)

    dims = scene.add_object_to(plate, cake, 'on_right')
    dims = scene.add_object_to(table, pen, 'on_right')
    dims = scene.add_object_to(table, chair, 'left')
    chair.start = dims.get('start')
    chair.end = dims.get('end')

    dims = scene.add_object_to(chair, plate, 'center', add_y = 400)
    dims = scene.add_object_to(table, book, 'on_left')
    dims = scene.add_object_to(table, book, 'under')
    scene.save_image()

#############################################################################################
