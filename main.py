from Util import Module_Ssh

# 예제 사용
if __name__ == "__main__":
    # SSH 연결 정보
    host = 'localhost'
    port = 2222  # SSH 포트 (기본값은 22)
    username = 'root'
    password = 'root'

    # SSH 클라이언트 인스턴스 생성
    ssh_client = Module_Ssh.ModuleSsh(host, port, username, password)

    # SSH 연결
    if ssh_client.connect():
        # 실행할 명령어
        command = 'ls -l /'  # 예시 명령어

        # 명령어 실행
        ssh_client.execute_command(command)

        # SSH 연결 종료
        ssh_client.close()
