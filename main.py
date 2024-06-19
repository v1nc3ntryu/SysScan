from Util.Module_Ssh import *
from Scan.CheckOs import *
from Scan.ScanSystem import *
from Scan.ScanNetwork import *
from Scan.ScanAccount import *
from Scan.ScanLog import *

def init_scan(ssh_client):
    json_result = {}
    str_result = ''

    os_type = CheckOs(ssh_client).os_type

    scanSystem = ScanSystem(ssh_client, os_type)
    scanNetwork = ScanNetwork(ssh_client, os_type)
    scanAccount = ScanAccount(ssh_client, os_type)
    # scanLog = ScanLog(ssh_client, os_type)

    json_result.update(scanSystem.json_result)
    json_result.update(scanNetwork.json_result)
    json_result.update(scanAccount.json_result)
    # json_result.update(scanLog.json_result)

    str_result += scanSystem.str_result
    str_result += scanNetwork.str_result
    str_result += scanAccount.str_result
    # str_result += scanLog.str_result

    file_write(json.dumps(json_result, indent=4), 'raw.json')
    file_write(str_result, 'raw.txt')

if __name__ == "__main__":
    ssh_client = ModuleSsh()
    if ssh_client.connect() == True:
        init_scan(ssh_client)
    else:
        print('SSH Connect Failed')
    ssh_client.close()
