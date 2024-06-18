from Util.Common import *

class CheckOs:
    def __init__(self, ssh_client):
        self.ssh_client = ssh_client
        self.class_name = type(self).__name__
        print(f'\n[{self.class_name}]')
        self.os_type = 'L'
        self.sudo = False
        self.check_os_type()
        self.check_sudo()

    def check_os_type(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        command = 'ls -al'
        raw_result = self.ssh_client.execute_command(command)
        if raw_result.startswith('total') == False:
            self.os_type = 'W'
        print(f'os type is :{self.os_type}')

    def check_sudo(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        if self.os_type == 'L':
            command = '-l'
            raw_result = self.ssh_client.execute_command(command, use_sudo=True)
            if 'not' in raw_result:
                self.sudo = True
            print(f'Is sudo :{self.sudo}')
