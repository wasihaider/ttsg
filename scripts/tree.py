#############################################################################################
class Node:
    """
    This class will have objects which are nodes of a tree
    It will contain all data related to single object e-g table
    """
    def __init__(self, name, determiner, adjectives):
        self.name = name
        self.determiner = determiner
        self.adjectives = []
        self.relation_to_parent = None
        for adjective in adjectives:
            self.adjectives.append(adjective)  # to avoid same pointer
        self.children = []  # list of children because the tree will be a general tree
        self.id = -1
        self.level = -1
        self.image = None

    ######################################################

    def __str__(self):
        return "Name: {}\nID: {}\nLevel: {}\nDeterminer: {}\nAdjectives: {}".format(
            self.name,
            self.id,
            self.level,
            self.determiner,
            self.adjectives
        )

    ######################################################

    def put_child(self, parent, node, relation):
        """
        This method insert a new child of a node in its child list
        :param parent: parent node of the object to insert, if any
        :param node: the node to insert
        :return {'added': True, 'recentObject': node}: if the node is added successfully
        :return {'added: False, 'recentObject': None}: if node is not added
        """
        try:
            if self.is_equal(parent):
                node.id = self.number_of_children()
                node.level = self.level + 1
                node.relation_to_parent = relation
                self.children.append(node)
                return {'added': True, 'recentObject': node}
            else:
                result = {'added': False, 'recentObject': None}
                for child in self.children:
                    result = child.put_child(parent, node, relation)
                    if result.get("added"):
                        break
                return result
        except Exception as e:
            print("Exception in tree.py, Class Node (put_child method): ", str(e))

    ######################################################

    def number_of_children(self):
        """
        This method return the number of children of the node on which it is called
        :return length: number of children of current node
        """
        return len(self.children)

    ######################################################

    def is_equal(self, node):
        """
        This method check if the data of self node with the node provided in param is equal or not
        :param node: The node to compare with self node
        :return True: if equal
        :return False: if not equal
        """
        try:
            if self.id == node.id and self.level == node.level and self.name == node.name:
                return True
            else:
                return False
        except Exception as e:
            print("Exception in tree.py, Class Node (is_equal method): ", str(e))

    ######################################################

    def print_tree_nodes(self):
        """
        This method print the tree from the self node it is called on
        :return: Returns nothing
        """
        try:
            tabs = ""
            for i in range(self.level):
                tabs = tabs + '\t'
            print("{}+{}({},{}) - {}".format(tabs, self.name, self.id, self.level, self.relation_to_parent))
            if self.number_of_children() is not 0:
                for child in self.children:
                    child.print_tree_nodes()
            else:
                return
        except Exception as e:
            print("Exception in tree.py, Class Node (print_tree_nodes method: )", str(e))


#############################################################################################

class GenerateTree:
    """
    This class will generate the tree using the nodes given
    This class will also maintain the recent added object and all recent parents added to keep a track
    """

    def __init__(self):
        self.recentObject = None  # Recent object added to the tree
        self.recentParent = {}  # Recent Parents added to tree for every object of the project
        self.roots = []  # in case there are more objects with no parents

    ######################################################

    def add_node(self, parent, node, relation):
        """
        This method adds the node to tree in its right position(below its parent)
        If the parent does not exists this method will create a new parent as another root of tree
        :param relation: The preposition (relation) between the objects
        :param parent: The parent of the node to be added, if any
        :param node: The node to be added to tree
        :return: returns nothing
        """
        try:
            if parent is None:  # if parent is none then the node is a root object
                node.id = self.num_roots()
                node.level = 0
                node.relation_to_parent = relation
                self.roots.append(node)
                self.recentObject = node
                self.recentParent[node.name] = node
            elif self.num_roots() is 0:  # if there is no root then add parent as root and node as child of it
                root = Node(parent.name, parent.determiner, parent.adjectives)
                root.id = parent.id = self.num_roots()
                root.level = parent.level = 0
                result = root.put_child(parent, node, relation)

                self.roots.append(root)
                self.recentObject = result.get("recentObject")
                self.recentParent[parent.name] = parent
                self.recentParent[node.name] = node
            else:
                for root in self.roots:
                    result = root.put_child(parent, node, relation)
                    if result.get("added"):
                        break
                if result.get("added"):  # if node is added
                    self.recentObject = result.get("recentObject")
                    self.recentParent[parent.name] = parent
                    self.recentParent[node.name] = node
                else:  # if node is not added then first add the parent as root and then node as its child
                    parent.id = self.num_roots()
                    parent.level = 0
                    result = parent.put_child(parent, node, relation)
                    self.roots.append(parent)
                    self.recentObject = result.get('recentObject')
                    self.recentParent[parent.name] = parent
                    self.recentParent[node.name] = node
        except Exception as e:
            print("Exception in tree.py, Class GenerateTree (add_node method: )", str(e))

    ######################################################

    def num_roots(self):
        """
        This method is to get the number of independent trees or roots
        :return length: number of roots
        """
        return len(self.roots)

    ######################################################

    def recent_parent_of(self, key):
        """
        This method is to get recent parent of a specific object type
        :param key: the object name to find in recent parents
        :return Node: the recent parent as Node object
        :return None: if no data found
        """
        try:
            if key in self.recentParent.keys():
                return self.recentParent.get(key)
            else:
                return None
        except Exception as e:
            print("Exception in tree.py, Class GenerateTree (recent_parent_of method: )", str(e))

    ######################################################

    def print_tree(self):
        """
        This method prints all the nodes of tree
        :return: Returns nothing
        """
        try:
            for root in self.roots:
                root.print_tree_nodes()
        except Exception as e:
            print("Exception in tree.py, Class GenerateTree (print_tree method: )", str(e))


#############################################################################################

if __name__ == '__main__':
    table = Node("table")
    chair = Node("chair")
    plate = Node("plate")
    book = Node("book")

    tree = GenerateTree()

    tree.add_node(table, chair)

    recentParent = tree.recentParent.get("table")
    tree.add_node(recentParent, plate)

    recentParent = Node(chair.name)
    recentParent.id = chair.id
    recentParent.level = chair.level
    anotherplate = Node("plate")
    tree.add_node(recentParent, anotherplate)
    tree.add_node(recentParent, book)

    cake = Node("cake")
    recentParent = Node(plate.name)
    recentParent.id = plate.id
    recentParent.level = plate.level
    tree.add_node(recentParent, cake)

    chairs = Node("chair")
    pen = Node("pen")
    tree.add_node(chairs, pen)

    tree.print_tree()

#############################################################################################
