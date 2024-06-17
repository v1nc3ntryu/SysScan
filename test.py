import json

def convert_tree_json(tree_json):
    def process_node(node):
        if node["type"] == "directory":
            contents = []
            for item in node.get("contents", []):
                contents.append(process_node(item))
            return {node["name"]: contents}
        elif node["type"] == "file":
            return node["name"]

    result = []
    for item in tree_json:
        result.append(process_node(item))
    
    return result
