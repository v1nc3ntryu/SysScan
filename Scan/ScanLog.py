from Util.Common import *

class ScanLog:
    def __init__(self, ssh_client, os_type):
        self.ssh_client = ssh_client
        self.class_name = type(self).__name__
        print(f'\n[{self.class_name}]')
        self.json_result = {}
        self.str_result = ''
        self.os_type = os_type

        self.info_history()
        self.json_result = {'scan_log' : self.json_result}


    def info_history(self):
        method_name = inspect.currentframe().f_code.co_name
        print(f'[*] {method_name}...')
        commands = [
            'history',
        ]
        raw_result = ''
        for command in commands:
            raw_result_temp = self.ssh_client.execute_command(command)
            raw_result += f'\nCommand : {command}'
            raw_result += f'\nRaw Result :\n'
            raw_result += f'\n{raw_result_temp}'
                
        gather_result_json(self.json_result, method_name, 'Check txt Result')
        self.str_result = gather_result_multi(self.str_result, self.class_name, method_name, raw_result)

