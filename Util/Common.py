import inspect, json, os

def gather_result_json(json_result, method_name, result):
    json_result.update({method_name : result})

def gather_result(str_result, class_name, method_name, command, raw_result):
    str_result += f'\n--------------------------------------'
    str_result += f'\nClass Name : {class_name}'
    str_result += f'\nMethod Name : {method_name}'
    str_result += f'\nCommand : {command}'
    str_result += f'\nRaw Result :\n'
    str_result += f'\n{raw_result}'
    return str_result

def gather_result_multi(str_result, class_name, method_name, raw_result):
    str_result += f'\n--------------------------------------'
    str_result += f'\nClass Name : {class_name}'
    str_result += f'\nMethod Name : {method_name}'
    str_result += f'{raw_result}'
    return str_result

def file_write(raw_file, file_name):
    current_dir = os.path.join(os.getcwd(), 'Result')

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)  # 'Result' 디렉토리가 없으면 생성
        
    with open(current_dir + f'/{file_name}', 'w') as file:
        file.write(raw_file)

def parse_tree_linux(tree_text):
    tree_text = json.loads(tree_text)
    if len(tree_text) < 2:
        return {}
    
    def process_node(node):
        if 'error' not in node:
            if node["type"] == "directory":
                contents = []
                for item in node.get("contents", []):
                    processed_item = process_node(item)
                    if processed_item:  # None이 아닌 경우만 추가
                        contents.append(process_node(item))
                return {node["name"]: contents}
            elif node["type"] == "file":
                return node["name"] if node["name"] is not None else None

    result = []
    for item in tree_text:
        processed_item = process_node(item)
        if processed_item:  # None이 아닌 경우만 추가
            result.append(process_node(item))

    if len(result) > 0:
        if '/' in result[0]:
            result = result[0]['/']

    return result

        

