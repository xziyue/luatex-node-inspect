from graphviz import Digraph
import json

with open('../temp.json', 'r') as infile:
    obj = json.load(infile)

root = obj

class GraphBuilder:

    important_fields = [
        'width', 'height', 'data', 'char'
    ]

    unimportant_fields = [
        'attr'
    ]

    def __init__(self):
        self.node_counter = 0
        self.graph = Digraph()
        self.graph.graph_attr['rankdir'] = 'LR'

    def generate_helper(self, node, last_id):
        if isinstance(node, dict):
            # create a id for this node
            my_id = self.node_counter
            self.node_counter += 1
            node_text = ['<B>%s</B>' % node["id"]]
            if "whatsit" in node["id"]:
                node_text.append('<B>%s</B>' % node["subtype"])
            for key, val in node.items():
                if key in self.unimportant_fields:
                    continue
                elif isinstance(val, list):
                    for item in val:
                        self.generate_helper(item, my_id)
                elif isinstance(val, dict):
                    self.generate_helper(val, my_id)
                else:
                    if key in self.important_fields:
                        node_text.append('{}={}'.format(key, val))

            node_str = '<BR/>'.join(node_text)
            my_node = self.graph.node(str(my_id), '<%s>'%node_str)
            if last_id > -1:
                self.graph.edge(str(last_id), str(my_id))

    def generate(self, node):
        self.generate_helper(node, -1)


gb = GraphBuilder()
gb.generate(root)
gb.graph.render('node', renderer='cairo', format='svg')