import paramiko
import time
from Util.Static import *
# from Static import *

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

    def execute_command(self, command):
        if not self.client:
            print("\n[-] SSH client is not connected.")
            return None
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            time.sleep(0.5)  # 명령 실행 대기
            try:
                output = stdout.read().decode()
                error = stderr.read().decode()
            except UnicodeDecodeError as e:
                # print(f"[-] UnicodeDecodeError: {e}")
                # print('may be windows')
                output = stdout.read().decode('cp1252')
                error = stderr.read().decode('cp1252')
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