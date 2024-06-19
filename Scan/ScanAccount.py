from Util.Common import *

class ScanAccount:
    def __init__(self, ssh_client, os_type):
        self.ssh_client = ssh_client
        self.class_name = type(self).__name__
        print(f'\n[{self.class_name}]')
        self.json_result = {}
        self.str_result = ''
        self.os_type = os_type

        self.info_user()
        self.info_group()
        self.info_pam()
        self.json_result = {'scan_account' : self.json_result}


    def info_user(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        raw_result = ''
        result = {}

        if self.os_type == 'L':
            command = 'cat /etc/passwd'
            raw_result = self.ssh_client.execute_command(command)
            for line in raw_result.split('\n'):
                parts = line.strip().split(':')
                if len(parts) < 2:
                    continue
                user_info = {
                    'uid': parts[2],
                    'gid': parts[3],
                    'comment': parts[4],
                    'home_directory': parts[5],
                    'login_shell': parts[6]
                }
                result[parts[0]] = user_info

        elif self.os_type == 'W':
            command = 'ipconfig'
            raw_result = self.ssh_client.execute_command(command)
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_group(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        raw_result = ''
        result = {}

        if self.os_type == 'L':
            command = 'cat /etc/group'
            raw_result = self.ssh_client.execute_command(command)
            for line in raw_result.split('\n'):
                parts = line.strip().split(':')
                if len(parts) < 2:
                    continue
                group_info = {
                    'gid': parts[2],
                    'members': parts[3].split(',') if parts[3] else []
                }
                result[parts[0]] = group_info

        elif self.os_type == 'W':
            command = 'ipconfig'
            raw_result = self.ssh_client.execute_command(command)
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    def info_pam(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        commands = [
            'cat /etc/pam.d/sshd',
        ]
        raw_result = ''
        for command in commands:
            raw_result_temp = self.ssh_client.execute_command(command)
            raw_result += f'\nCommand : {command}'
            raw_result += f'\nRaw Result :\n'
            raw_result += f'\n{raw_result_temp}'
                
        gather_result_json(self.json_result, method_name, 'Check txt Result')
        self.str_result = gather_result_multi(self.str_result, self.class_name, method_name, raw_result)
