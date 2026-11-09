FROM debian:bookworm-slim

RUN apt-get update && apt-get install -y \
    openjdk-17-jdk-headless \
    python3 \
    python3-pip \
    python3-pandas \
    python3-psycopg2 \
    openssh-server \
    curl \
    tar \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN curl -sL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | tar -xz -C /opt/ \
    && mv /opt/hadoop-${HADOOP_VERSION} $HADOOP_HOME

RUN useradd -m -s /bin/bash hadoopuser && \
    echo "hadoopuser:hadoopuser" | chpasswd && \
    mkdir -p /home/hadoopuser/.ssh && \
    ssh-keygen -t rsa -P "" -f /home/hadoopuser/.ssh/id_rsa && \
    cat /home/hadoopuser/.ssh/id_rsa.pub >> /home/hadoopuser/.ssh/authorized_keys && \
    chmod 700 /home/hadoopuser/.ssh && \
    chmod 600 /home/hadoopuser/.ssh/authorized_keys && \
    chown -R hadoopuser:hadoopuser /home/hadoopuser/.ssh

RUN mkdir /var/run/sshd

WORKDIR /app

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
