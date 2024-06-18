import paramiko
import time
# from Util.Static import *
from Static import *

class ModuleSsh:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.username = USERNAME
        self.password = PASSWORD
        self.sudo_password = PASSWORD  # sudo 비밀번호를 추가
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
            print(f"[+] Connected to {self.host} via SSH\n")
        except Exception as e:
            print(f"[-] Failed to connect to {self.host}: {e}\n")
            return False
        return True

    def execute_command(self, command, use_sudo=False):
        if not self.client:
            print("\n[-] SSH client is not connected.")
            return None
        
        try:
            if use_sudo:
                # sudo 명령어를 실행하기 위한 채널 생성
                channel = self.client.invoke_shell()
                time.sleep(1)  # 채널 초기화 대기
                channel.send('sudo ' + command + '\n')

                # sudo 비밀번호 입력 대기
                buff = ''
                while not channel.recv_ready():
                    time.sleep(0.1)
                
                while channel.recv_ready():
                    resp = channel.recv(9999)
                    buff += resp.decode('utf-8')
                
                # if '[sudo] password for ' + self.username + ':' in buff:
                #     channel.send(self.sudo_password + '\n')
                
                # 명령어 출력 대기
                buff = ''
                while True:
                    while channel.recv_ready():
                        time.sleep(0.1)
                        resp = channel.recv(9999)
                        buff += resp.decode('utf-8')
                        print(buff)
                        if '[sudo] password for' in buff:
                            print('password time!!')
                            channel.send(self.sudo_password + '\n')
                            break
                    print(f'>>> {buff}')
                    if buff.endswith('$ ') or buff.endswith('# '):  # 쉘 프롬프트 확인
                        break
                    time.sleep(0.1)
                print(f'||| {buff}')
                return buff
            else:
                stdin, stdout, stderr = self.client.exec_command(command)
                time.sleep(0.5)  # 명령 실행 대기
                output = stdout.read().decode()
                error = stderr.read().decode()
                if error:
                    return error
                else:
                    return output
        except Exception as e:
            print(f"\n[-] Unexpected Error: {e}")
            return None

    def close(self):
        if self.client:
            self.client.close()
            print(f"\n[+] Connection to {self.host} closed.")

# Example usage:
if __name__ == "__main__":
    ssh = ModuleSsh()
    if ssh.connect():
        print(ssh.execute_command('ls /root', use_sudo=True))
        ssh.close()
