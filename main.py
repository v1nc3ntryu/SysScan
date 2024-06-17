from Util.Module_Ssh import *
from Scan.ScanSystem import *

def init_scan(ssh_client):
    json_result = {}
    str_result = ''

    scan_system = ScanSystem(ssh_client)

    json_result.update(scan_system.json_result)
    str_result += scan_system.str_result

    write_json(json_result)
    write_str(str_result)
    

# 예제 사용
if __name__ == "__main__":
    # SSH 클라이언트 인스턴스 생성
    ssh_client = ModuleSsh()

    # SSH 연결
    if ssh_client.connect() == True:
        init_scan(ssh_client)
    
    else:
        print('SSH Connect Failed')

    ssh_client.close()
