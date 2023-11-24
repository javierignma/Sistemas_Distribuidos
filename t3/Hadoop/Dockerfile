FROM eclipse-temurin:8-jdk-focal

# Instalación de paquetes necesarios y limpieza en un solo paso RUN para reducir capas y tamaño de imagen
RUN apt-get update -y \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y --no-install-recommends \
        sudo \
        curl \
        ssh \
        python3 \
        python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalación de paquetes de Python necesarios
RUN pip3 install requests

# Configuración del usuario hduser y configuraciones relacionadas con sudo
RUN useradd -m hduser \
    && echo "hduser:supergroup" | chpasswd \
    && adduser hduser sudo \
    && echo "hduser     ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers \
    && ln -s /usr/bin/python3 /usr/bin/python

COPY ssh_config /etc/ssh/ssh_config

# Configuración de claves SSH para el usuario hduser
USER hduser
WORKDIR /home/hduser
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 0600 ~/.ssh/authorized_keys

# Descarga y configuración de Hadoop
ENV HADOOP_VERSION=3.3.3
ENV HADOOP_HOME=/home/hduser/hadoop-${HADOOP_VERSION}
RUN curl -sL --retry 3 \
  "http://archive.apache.org/dist/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz" \
  | gunzip \
  | tar -x -C /home/hduser/ \
 && rm -rf ${HADOOP_HOME}/share/doc

# Configuración de variables de entorno para Hadoop
ENV HDFS_NAMENODE_USER=hduser \
    HDFS_DATANODE_USER=hduser \
    HDFS_SECONDARYNAMENODE_USER=hduser \
    YARN_RESOURCEMANAGER_USER=hduser \
    YARN_NODEMANAGER_USER=hduser \
    PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN echo "export JAVA_HOME=/opt/java/openjdk/" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Copia de archivos de configuración y script de entrada
COPY core-site.xml hdfs-site.xml yarn-site.xml $HADOOP_HOME/etc/hadoop/
COPY docker-entrypoint.sh /usr/local/bin/
RUN sudo chmod +x /usr/local/bin/docker-entrypoint.sh

# Exposición de puertos necesarios para Hadoop
EXPOSE 50070 50075 50010 50020 50090 8020 9000 9864 9870 10020 19888 8088 8030 8031 8032 8033 8040 8042 22

# Configuración para prevenir la iniciación automática de YARN
ENV YARNSTART=0

# Configuración del ENTRYPOINT con el script de entrada
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]