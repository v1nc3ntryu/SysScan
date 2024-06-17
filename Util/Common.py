import inspect, json, os

def gather_result(json_result, str_result, result, class_name, method_name, command, raw_result):
    json_result.update({method_name : result})
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

def write_json(raw_json):
    current_dir = os.path.join(os.getcwd(), 'Result')

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)  # 'Result' 디렉토리가 없으면 생성
        
    with open(current_dir + '/raw.json', 'w') as file:
            file.write(json.dumps(raw_json, indent=4))

def write_str(raw_str):
    current_dir = os.path.join(os.getcwd(), 'Result')

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)  # 'Result' 디렉토리가 없으면 생성
        
    with open(current_dir + '/raw.txt', 'w') as file:
            file.write(raw_str)