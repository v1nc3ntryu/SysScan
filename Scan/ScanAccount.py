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
        # self.info_pam()
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
            command = 'chcp 437 && net user'
            raw_result = self.ssh_client.execute_command(command).replace('\r', '')
            check = False
            temp = []
            for line in raw_result.split('\n'):
                if check == False:
                    if '--------' in line:
                        check = True
                elif check == True and 'The command completed successfully' in line:
                    break
                else:
                    temp.extend(line.split(' '))
            raw_result = ''
            for user in temp:
                if user != '':
                    command = f'chcp 437 && net user {user}'
                    raw_result_temp = self.ssh_client.execute_command(command).replace('\r', '')
                    raw_result += raw_result_temp
                    user_info = {
                        'full_name': '',
                        'account_active': '',
                        'comment': '',
                        'home_directory': '',
                        'last_logon': ''
                    }
                    for line in raw_result_temp.split('\n'):
                        if 'Full Name' in line:
                            user_info['full_name'] = line.split('Full Name')[-1].lstrip()
                        elif 'Account active' in line:
                            user_info['account_active'] = line.split('Account active')[-1].lstrip()
                        elif 'Comment' in line:
                            user_info['comment'] = line.split('Comment')[-1].lstrip()
                        elif 'Home directory' in line:
                            user_info['home_directory'] = line.split('Home directory')[-1].lstrip()
                        elif 'Last logon' in line:
                            user_info['last_logon'] = line.split('Last logon')[-1].lstrip()
                    result[user] = user_info
                    
            command = 'chcp 437 && net user {user}'

                
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
            command = 'chcp 437 && net localgroup'
            raw_result = self.ssh_client.execute_command(command).replace('\r', '')
            check = False
            temp = []
            for line in raw_result.split('\n'):
                if check == False:
                    if '--------' in line:
                        check = True
                elif check == True and 'The command completed successfully' in line:
                    break
                else:
                    temp.append(line.replace('*', ''))

            raw_result = ''
            for group in temp:
                command = f'chcp 437 && net localgroup "{group}"'
                raw_result_temp = self.ssh_client.execute_command(command).replace('\r', '')
                raw_result += raw_result_temp

                group_info = {
                    'comment': '',
                    'members': [],
                }
                check = False
                for line in raw_result_temp.split('\n'):
                    if check == False:
                        if line.startswith('Comment'):
                            group_info['comment'] = line.split('Comment')[-1].lstrip()
                        elif line.startswith('-------------------'):
                            check = True
                    elif check == True and 'The command completed successfully' in line:
                        break
                    else:
                        group_info['members'].append(line)
                    
                result[group] = group_info
                    
            command = 'chcp 437 && net localgroup {group}'
                
        gather_result_json(self.json_result, method_name, result)
        self.str_result = gather_result(self.str_result, self.class_name, method_name, command, raw_result)


    # def info_pam(self):
    #     method_name = inspect.currentframe().f_code.co_name
    #     print(f'[*] {method_name}...')
    #     commands = [
    #         'cat /etc/pam.d/sshd',
    #     ]
    #     raw_result = ''
    #     for command in commands:
    #         raw_result_temp = self.ssh_client.execute_command(command)
    #         raw_result += f'\nCommand : {command}'
    #         raw_result += f'\nRaw Result :\n'
    #         raw_result += f'\n{raw_result_temp}'
                
    #     gather_result_json(self.json_result, method_name, 'Check txt Result')
    #     self.str_result = gather_result_multi(self.str_result, self.class_name, method_name, raw_result)
