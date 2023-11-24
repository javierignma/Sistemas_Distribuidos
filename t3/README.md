# Tarea 3 Sistemas Distribuidos
Integrantes: Pablo Lores y Javier Molina

Primero levantar el servicio de Hadoop con : `sudo docker-compose up -d` o utilizar `sudo docker compose up -d`

Después ejecutar el servicio Hadoop con: `sudo docker exec -it hadoop bash`

Copiar y pegar la siguiente secuencia de comandos para generar los datos con índice invertido:
```
hdfs dfs -mkdir /user
hdfs dfs -mkdir /user/hduser
hdfs dfs -mkdir input
sudo chown -R hduser .
cd map-reduce/
hdfs dfs -put carpeta1/*.txt input
hdfs dfs -put carpeta2/*.txt input
mapred streaming -files mapper.py,reducer.py -input /user/hduser/input/*.txt -output hduser/outhadoop/ -mapper ./mapper.py -reducer ./reducer.py
hdfs dfs -get /user/hduser/hduser/outhadoop/ /home/hduser/map-reduce

```
Los datos se guardarán en la carpeta outhadoop.