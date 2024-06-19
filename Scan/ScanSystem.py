from Util.Common import *

class ScanSystem:
    def __init__(self, ssh_client, os_type):
        self.ssh_client = ssh_client
        self.class_name = type(self).__name__
        print(f'\n[{self.class_name}]')
        self.json_result = {}
        self.str_result = ''
        self.os_type = os_type

        self.info_os()
        self.info_service()
        self.info_env()
        self.info_cron()
        self.json_result = {'scan_system' : self.json_result}


    def info_os(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        result = ''
        
        if self.os_type == 'L':
            command = 'cat /etc/os-release'
            raw_result = self.ssh_client.execute_command(command)
            lines = raw_result.split('\n')
            for line in lines:
                if line.startswith('PRETTY_NAME'):
                    result = line.strip().split('=')[-1].strip('"')

        elif self.os_type == 'W':
            command = 'ver'
            raw_result = self.ssh_client.execute_command(command)
            result = raw_result.replace('\n', '').replace('\r', '')
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_service(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        result = {}
        
        if self.os_type == 'L':
            command = 'service --status-all'
            raw_result = self.ssh_client.execute_command(command)
            for line in raw_result.split('\n'):
                line = line.replace(']', '')
                line = line.replace('[', '')
                parts = line.split()
                if len(parts) < 1:
                    continue
                result.update({parts[1] : 'on' if parts[0] == '+' else 'off'})

        elif self.os_type == 'W':
            command = ''
            raw_result = ''
            result = {}
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_env(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        result = {}
        
        if self.os_type == 'L':
            command = 'printenv'
            raw_result = self.ssh_client.execute_command(command)
            for line in raw_result.split('\n'):
                temp_result = line.strip().split('=')
                if len(temp_result) < 2:
                    continue
                result.update({temp_result[0] : temp_result[1]})

        elif self.os_type == 'W':
            command = 'set'
            raw_result = self.ssh_client.execute_command(command)
            for line in raw_result.split('\n'):
                temp_result = line.strip().split('=')
                if len(temp_result) < 2:
                    continue
                result.update({temp_result[0] : temp_result[1]})
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_cron(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        result = {}
        
        
        if self.os_type == 'L':
            command = 'crontab -l'
            raw_result = self.ssh_client.execute_command(command)
            if 'not found' not in raw_result:
                for line in raw_result.split('\n'):
                    line = line.lstrip()
                    if line.startswith('#') or line == '':
                        continue
                    else:
                        parts = line.split(' ')
                        cron_info = {
                            'minute' : parts[0],
                            'hour' : parts[1],
                            'day_of_month' : parts[2],
                            'month' : parts[3],
                            'day of week' : parts[4],
                        }
                        result[parts[5]] = cron_info
            else:
                result['no crontab'] = ''

        elif self.os_type == 'W':
            # 결과가 안보임..
            command = 'schtasks /query /fo LIST /v'
            raw_result = self.ssh_client.execute_command(command)
            result = 'check txt result'
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)
