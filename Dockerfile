# 베이스 이미지로 Ubuntu 사용
FROM ubuntu:latest

# 패키지 목록 업데이트 및 OpenSSH 서버 설치
RUN apt-get update && apt-get install -y openssh-server

# SSH 데몬을 실행하기 위한 디렉터리 생성
RUN mkdir /var/run/sshd

# root 사용자의 비밀번호 설정
RUN echo 'root:root' | chpasswd

# PermitRootLogin을 허용하도록 sshd_config 수정
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH 접속을 위해 포트 22 노출
EXPOSE 22

# SSH 데몬 실행
CMD ["/usr/sbin/sshd", "-D"]

# docker build -t ubuntu-ssh .
# docker run -d -p 2222:22 ubuntu-ssh