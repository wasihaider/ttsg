from __future__ import unicode_literals
from nltk import word_tokenize, pos_tag, sent_tokenize, RegexpParser

#############################################################################################

# def generateTree

#############################################################################################
from Sentence_Parsing import SentenceParser
from tree import GenerateTree

tree = GenerateTree()


def add_node_to_tree(objects):
    parent = objects.get('parent')
    child = objects.get('child')
    it = objects.get('case_it')

    if parent is None:
        tree.add_node(parent, child)
        return
    elif it:
        recent_object = tree.recentObject
        if parent.name == 'it':
            tree.add_node(recent_object, child)
        else:
            tree.add_node(parent, recent_object)
        return
    elif parent.determiner.lower() == "the":
        recent_parent = tree.recentParent.get(parent.name)
        if recent_parent is None:
            tree.add_node(parent, child)
        else:
            tree.add_node(recent_parent, child)
    else:
        tree.add_node(parent, child)


def main():
    paragraph = """There was a table in the Room.
    The table was near a chair.
    the table has a plate on it.
    the plate has a cake on it"""
    sentences = sent_tokenize(paragraph)
    for sentence in sentences:
        parser = SentenceParser(sentence)
        objectss = parser.objects_with_relation()
        add_node_to_tree(objectss)

    tree.print_tree()
    print(tree.recentParent)


if __name__ == '__main__':
    sentence = "The chair was on left side of the table"
    words = word_tokenize(sentence)
    tagged = pos_tag(words)
    print(tagged)
# nltk.help.upenn_tagset()
