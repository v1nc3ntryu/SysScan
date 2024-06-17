import json, os

def write_json(raw_json):
    current_dir = os.path.join(os.getcwd(), 'Result')

    if not os.path.exists(current_dir):
        os.makedirs(current_dir)  # 'Result' 디렉토리가 없으면 생성
        
    with open(current_dir + '/test.json', 'w') as json_file:
            json_file.write(json.dumps(raw_json, indent=4))


write_json({})