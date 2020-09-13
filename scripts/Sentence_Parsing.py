from nltk import word_tokenize, pos_tag, RegexpParser
from scripts.Find_Parent_Dataset import DatasetPreprocessing
from keras.models import load_model
import numpy as np
from scripts.tree import Node
from scripts.constants_ttsg import SCRIPTS_DIR


#############################################################################################

class SentenceParser:
    """
    This class will be used for sentence parsing
    To extract objects and their relations to populate the tree
    To know the type of the sentence
    """

    def __init__(self, sentence):
        self.sentence = sentence
        self.__parent = None
        self.__child = None

    ######################################################

    def __sentence_parent_type(self):
        """
        This method will find the type of the sentence
        :return 1: if the first object is parent
        :return 0: if the second object is parent
        """
        try:
            dp = DatasetPreprocessing()
            sentence = [self.sentence]
            transformed_sentence = dp.transform(sentence)
            model_path = "".join([SCRIPTS_DIR, "FindParentMode.h5"])
            model = load_model(model_path)
            predictions = model.predict(transformed_sentence)
            label = np.argmax(predictions)
            return label
        except Exception as e:
            print("Exception in Sentence_Parsing.py (__sentence_parent_type method): ", str(e))

    ######################################################

    def objects_with_relation(self):
        """
        This method will generates a tree which will have chunks of specific regex given
        :return dict: parent child Node class objects and relation between them
        """
        try:
            words = word_tokenize(self.sentence)
            tagged = pos_tag(words)
            regex = r"chunk: {(<DT>*<JJ>*<NN>)?<PRP>?}"
            regex2 = r"chunk: {(<DT>*<JJ>*<NN>)<IN>(<DT>*<JJ>*<NN>)}"

            chunk_parser = RegexpParser(regex, root_label="S")
            chunks = chunk_parser.parse(tagged)
            trees = []
            for chunk in chunks.subtrees():
                if chunk.label() == 'chunk':
                    trees.append(chunk)

            objects = self.__list_of_objects(trees)
            for word, pos in tagged:
                if pos == 'IN':
                    objects['relation'] = word
                    break

            for word, pos in tagged:
                if word.lower() == "left" or word.lower() == "right":
                    objects['relation'] = word.lower()
                    break

            if 'relation' not in objects.keys():
                objects['relation'] = None

            # print("parent: {}\n, child: {}\n\n\n".format(objects.get('parent'), objects.get('child')))
            return objects
        except Exception as e:
            print("Exception in Sentence_Parsing.py (objects_with_relation method): ", str(e))

    ######################################################

    def __list_of_objects(self, trees):
        """
        This method parse the chunks and extract each different object and make it a node object
        :param trees: chunks to be parsed in Node objects
        :return dict: the dict of Node type objects {parent, child}
        :return None: if the chunks are more then two
        """
        try:
            type = self.__sentence_parent_type()
            objects = []
            case_it = False

            for tree in trees:
                data = {'adjectives': []}
                for word, pos in tree.leaves():
                    if pos == 'DT':
                        data['determiner'] = word.lower()
                    elif pos == 'JJ':
                        data['adjectives'].append(word.lower())
                    elif pos == 'NN' or pos == 'NNS':
                        if word.lower() != "left" and word.lower != "right":
                            data['name'] = word.lower()
                    elif pos == 'PRP':
                        if word.lower() != "left" and word.lower != "right":
                            data['name'] = word.lower()
                    else:
                        continue

                objects.append(Node(data.get('name'), data.get('determiner'), data.get('adjectives')))

            if len(objects) == 1:
                return {'parent': None, 'child': objects[0], 'case_it': case_it}

            if objects[0].name == 'it' or objects[1].name == 'it':
                case_it = True
            else:
                case_it = False

            if objects[0].name == 'room':
                parent = None
                child = objects[1]
            elif objects[1].name == 'room':
                parent = None
                child = objects[0]
            elif type == 0:
                parent = objects[0]
                child = objects[1]
            else:
                parent = objects[1]
                child = objects[0]

            return {'parent': parent, 'child': child, 'case_it': case_it}
        except Exception as e:
            print("Exception in Sentence_Parsing.py (__list_of_objects method): ", str(e))


#############################################################################################

if __name__ == '__main__':
    s = SentenceParser("table is on left of chair")

#############################################################################################
