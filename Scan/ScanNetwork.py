from Util.Common import *

class ScanNetwork:
    def __init__(self, ssh_client, os_type, sudo):
        self.ssh_client = ssh_client
        self.class_name = type(self).__name__
        print(f'\n[{self.class_name}]')
        self.json_result = {}
        self.str_result = ''
        self.os_type = os_type
        self.sudo = sudo

        self.info_ip()
        self.info_port()
        # self.info_firewall()
        # self.info_subnet_route()
        # self.info_ssh()
        # self.info_ids_ips()
        self.json_result = {'scan_network' : self.json_result}


    def info_ip(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        raw_result = ''
        result = {}

        if self.os_type == 'L':
            command = 'ifconfig'
            raw_result = self.ssh_client.execute_command(command)
            eth = ''
            for line in raw_result.split('\n'):
                if line.startswith(' ') or line == '':
                    line = line.lstrip()
                    if 'inet ' in line:
                        result[eth]['inet'] = line.split(' ')[1]
                    elif 'inet6 ' in line:
                        result[eth]['inet6'] = line.split(' ')[1]
                else:
                    temp = {
                        'inet' : '',
                        'inet6' : ''
                    }
                    eth = line.split(':')[0]
                    result.update({eth : temp})

        elif self.os_type == 'W':
            command = 'ipconfig'
            raw_result = self.ssh_client.execute_command(command)
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_port(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        raw_result = ''
        result = []

        if self.os_type == 'L':
            command = 'sudo netstat -tnlp'
            if self.sudo == True:
                raw_result = self.ssh_client.execute_command(command, use_sudo=True)
            else:
                raw_result = self.ssh_client.execute_command(command)
            check = False
            for line in raw_result.split('\n'):
                if check == False:
                    if 'Proto' in line:
                        check = True
                else:
                    temp1 = []
                    for temp_line in line.split(' '):
                        if temp_line != '':
                            temp1.append(temp_line)
                    if len(temp1) < 1:
                        continue
                    temp2 = temp1[0:-2]
                    pid = temp1[6]
                    pn = temp1[7]
                    temp2.append(pid + ' ' + pn)
                    temp3 = {
                        'protocol' : temp2[0],
                        'local_address' : temp2[3],
                        'foreign_address' : temp2[4],
                        'state' : temp2[5],
                        'pid/program_name' : temp2[6],
                    }
                    result.append(temp3)
            if len(result) < 1:
                result.append('no permission to check')
                

        elif self.os_type == 'W':
            command = 'ipconfig'
            raw_result = self.ssh_client.execute_command(command)
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_firewall(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        command = 'service --status-all'
        raw_result = self.ssh_client.execute_command(command)
        lines = raw_result.split('\n')
        result = []

        for line in lines:
            service = {
                'name':'',
                'status':'',
                'version':''
            }
            line = line.replace(']', '')
            line = line.replace('[', '')
            parts = line.split()
            if len(parts) < 1:
                continue
            # 서비스명
            service_name = parts[1]
            service['name'] = service_name
            # 서비스 상태
            service['status'] = 'on' if parts[0] == '+' else 'off'
            # 서비스 버전
            for version_check in ['-v', '-V', '--version']:
                version_command = f'{service_name} {version_check}'
                version_result = self.ssh_client.execute_command(version_command)
                if 'command not found' in version_result:
                    continue
                elif 'unknown option' in version_result:
                    continue
                elif 'usage' in version_result:
                    continue
                else:
                    service['version'] = version_result.replace('\n', '')
                    break
            result.append(service)
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_subnet_route(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        commands = [
            'cat /etc/passwd',
            'cat /etc/shadow'
        ]
        raw_result = ''
        for command in commands:
            raw_result_temp = self.ssh_client.execute_command(command)
            raw_result += f'\nCommand : {command}'
            raw_result += f'\nRaw Result :\n'
            raw_result += f'\n{raw_result_temp}'
                
        gather_result_json(self.json_result, method_name, 'Check txt Result')
        self.str_result = gather_result_multi(self.str_result, self.class_name, method_name, raw_result)


    def info_ssh(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        command = 'printenv'
        raw_result = self.ssh_client.execute_command(command)
        lines = raw_result.split('\n')
        result = []
        for line in lines:
            temp_result = line.strip().split('=')
            if len(temp_result) < 2:
                continue
            result.append({temp_result[0] : temp_result[1]})
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_ids_ips(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        command = 'crontab -l'
        raw_result = self.ssh_client.execute_command(command)
        lines = raw_result.split('\n')
        result = []
        if 'not found' not in raw_result:
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    result.append(line)
        else:
            result.append('no crontab')
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)

