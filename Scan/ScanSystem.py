from Util.Common import *

class ScanSystem:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client
        self.class_name = type(self).__name__
        print(f'[{self.class_name}]')
        self.json_result = {}
        self.str_result = ''

        self.info_os()
        self.info_service()
        self.info_system_file()
        self.info_env()
        self.info_cron()

        self.json_result = {'scan_system' : self.json_result}


    def info_os(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        command = 'cat /etc/os-release'
        raw_result = self.ssh_client.execute_command(command)
        lines = raw_result.split('\n')
        for line in lines:
            if line.startswith('PRETTY_NAME'):
                result = line.strip().split('=')[-1].strip('"')
                
        gather_results = [self.json_result, self.str_result, result, self.class_name, method_name, command, raw_result]
        self.str_result = gather_result(*gather_results)


    def info_service(self):
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
                
        gather_results = [self.json_result, self.str_result, result, self.class_name, method_name, command, raw_result]
        self.str_result = gather_result(*gather_results)


    def info_system_file(self):
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

        gather_results = [self.str_result, self.class_name, method_name, raw_result]
        self.str_result = gather_result_multi(*gather_results)


    def info_env(self):
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
                
        gather_results = [self.json_result, self.str_result, result, self.class_name, method_name, command, raw_result]
        self.str_result = gather_result(*gather_results)


    def info_cron(self):
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
                
        gather_results = [self.json_result, self.str_result, result, self.class_name, method_name, command, raw_result]
        self.str_result = gather_result(*gather_results)


    def info_directory(self):
        pass

    