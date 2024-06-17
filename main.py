from Util.Module_Ssh import *
from Scan.ScanSystem import *
from Scan.CheckOs import *

def init_scan(ssh_client):
    json_result = {}
    str_result = ''

    os_type = CheckOs(ssh_client).os_type
    str_result += get_result(ScanSystem(ssh_client, os_type), json_result, str_result)

    write_json(json_result)
    write_str(str_result)
    
def get_result(scanner, json_result, str_result):
    json_result.update(scanner.json_result)
    str_result += scanner.str_result
    return str_result

if __name__ == "__main__":
    ssh_client = ModuleSsh()
    if ssh_client.connect() == True:
        init_scan(ssh_client)
    else:
        print('SSH Connect Failed')
    ssh_client.close()
