FROM centos:7

# ADD http://mirrors.aliyun.com/repo/Centos-7.repo /etc/yum.repos.d/CentOS-Base.repo
# ADD http://mirrors.aliyun.com/repo/epel-7.repo /etc/yum.repos.d/epel.repo
RUN  yum makecache && yum install -y epel-release && yum install -y  python3-pip java-1.8.0-openjdk libaio  && rm -rf /var/cache/yum/* && yum clean all

ENV LC_CTYPE=en_US.UTF-8

WORKDIR /opt


RUN pip3 install --upgrade pip

WORKDIR /app
ADD ./server ./server
ADD ./core ./core
ADD ./main.py ./main.py
ADD ./.env.prod ./env
ADD ./requirements.txt ./requirements.txt

ENV APP_HOST 0.0.0.0
ENV APP_PORT 8080
ENV ENV prod

RUN pip3 install -r requirements.txt 

RUN useradd -u 1001 -ms /bin/bash  example
RUN mkdir -p /app/run
RUN chown -R 1001:1001 /app

USER example
CMD python /app/main.py
