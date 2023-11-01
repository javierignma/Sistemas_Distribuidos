# Tarea 2 de Sistemas Distribuidos: Apache Kafka.
Integrantes: Javier Molina y Vicente Castro

## Requisitos
1. `pip3 install kafka-python`
2. `pip3 install pandas`
3. `pip3 install confluent-kafka`

## Guía de uso
1. Ejecutar `sudo docker compose up -d` en el directorio raíz del proyecto.
2. Entrar en la carpeta consumers y ejecutar `python3 consumers.py`. Es importante ejecutar el .py dentro de la carpeta consumers.
3. Dentro de la carpeta producers, ejecutar `python3 master_huesillo.py <Nombre del maestro sin espacios> <isPaid (0=false and 1=True)>`.
  3.3. Este .py se puede ejecutar las veces que se necesite, pues representan los maestros. Abrir una nueva terminal por cada maestro a ejecutar.
4. En la carpeta db se podrá observar como se modifican los .csv.
5. Para reiniciar los .csv utilizar `python3 reset_db.py` dentro de la carpeta db. Importante que sea dentro de la carpeta db.
