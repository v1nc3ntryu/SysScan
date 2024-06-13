import paramiko
import time

class ModuleSsh:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self):
        try:
            self.client.connect(self.host, port=self.port, username=self.username, password=self.password)
            print(f"Connected to {self.host} via SSH")
        except Exception as e:
            print(f"Failed to connect to {self.host}: {e}")
            return False
        return True

    def execute_command(self, command):
        if not self.client:
            print("SSH client is not connected.")
            return None
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            time.sleep(1)  # 명령 실행 대기
            output = stdout.read().decode()
            error = stderr.read().decode()
            if error:
                print(f"Error executing command: {error}")
            else:
                print(f"Command execution successful:\n{output}")
            return output
        except Exception as e:
            print(f"Error executing command: {e}")
            return None

    def close(self):
        if self.client:
            self.client.close()
            print(f"Connection to {self.host} closed.")