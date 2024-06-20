from Util.Module_Ssh import *
from Scan.CheckOs import *
from Scan.ScanSystem import *
from Scan.ScanNetwork import *
from Scan.ScanAccount import *

# 정보 수집
def init_scan(ssh_client):
    json_result = {}
    str_result = ''

    # OS 종류 체크
    os_type = CheckOs(ssh_client).os_type

    # 시스템 정보 수집
    scanSystem = ScanSystem(ssh_client, os_type)
    # 네트워크 정보 수집
    scanNetwork = ScanNetwork(ssh_client, os_type)
    # 계정 정보 수집
    scanAccount = ScanAccount(ssh_client, os_type)

    # json 결과 merge
    json_result.update(scanSystem.json_result)
    json_result.update(scanNetwork.json_result)
    json_result.update(scanAccount.json_result)

    # txt 결과 merge
    str_result += scanSystem.str_result
    str_result += scanNetwork.str_result
    str_result += scanAccount.str_result

    # 파일로 출력
    file_write(json.dumps(json_result, ensure_ascii=False, indent=4), 'raw.json')
    file_write(str_result, 'raw.txt')

if __name__ == "__main__":
    # SSH 모듈 객체 생성
    ssh_client = ModuleSsh()

    # SSH 연결 시 정보 수집 진행
    if ssh_client.connect() == True:
        init_scan(ssh_client)
    else:
        print('SSH Connect Failed')

    # 프로세스 완료 후 SSH 종료
    ssh_client.close()
