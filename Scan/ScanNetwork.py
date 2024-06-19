from Util.Common import *

class ScanNetwork:
    def __init__(self, ssh_client, os_type):
        self.ssh_client = ssh_client
        self.class_name = type(self).__name__
        print(f'\n[{self.class_name}]')
        self.json_result = {}
        self.str_result = ''
        self.os_type = os_type

        self.info_ip()
        self.info_port()
        self.info_route()
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
                    # print(line.split(' '))
                    if 'inet ' in line:
                        result[eth]['inet'] = line.split(' ')[1]
                        if 'netmask ' in line:
                            result[eth]['netmask'] = line.split(' ')[4]
                    elif 'inet6 ' in line:
                        result[eth]['inet6'] = line.split(' ')[1]
                else:
                    temp = {
                        'inet' : '',
                        'inet6' : '',
                        'netmask' : '',
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
            command = 'ss -tuln'
            raw_result = self.ssh_client.execute_command(command)
            check = False
            for line in raw_result.split('\n'):
                if check == False:
                    if 'Netid' in line:
                        check = True
                else:
                    temp = []
                    for temp_line in line.split(' '):
                        if temp_line != '':
                            temp.append(temp_line)
                    if len(temp) < 1:
                        continue
                    temp3 = {
                        'protocol' : temp[0],
                        'state' : temp[1],
                        'port' : temp[4].split(':')[-1],
                        'local_address' : temp[4],
                        'peer_address' : temp[5],
                    }
                    result.append(temp3)
            if len(result) < 1:
                result.append('no module to check')
                

        elif self.os_type == 'W':
            command = 'ipconfig'
            raw_result = self.ssh_client.execute_command(command)
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_route(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        raw_result = ''
        result = {}

        if self.os_type == 'L':
            command = 'route -n'
            raw_result = self.ssh_client.execute_command(command)
            check = False
            for line in raw_result.split('\n'):
                if check == False:
                    if 'Destination' in line:
                        check = True
                else:
                    temp = []
                    for temp_line in line.split(' '):
                        if temp_line != '':
                            temp.append(temp_line)
                    if len(temp) < 1:
                        continue
                    iface = temp[7]
                    temp = {
                        'destination': temp[0],
                        'gateway': temp[1],
                        'genmask': temp[2],
                    }
                    result[iface] = temp

        elif self.os_type == 'W':
            command = 'ipconfig'
            raw_result = self.ssh_client.execute_command(command)
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


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
