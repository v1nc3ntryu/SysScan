from Util import Module_Ssh

# 예제 사용
if __name__ == "__main__":
    # SSH 클라이언트 인스턴스 생성
    ssh_client = Module_Ssh.ModuleSsh()

    # SSH 연결
    if ssh_client.connect() == False:
        pass
    
    command = 'ls -l /'  # 예시 명령어
    ssh_client.execute_command(command)



    ssh_client.close()
