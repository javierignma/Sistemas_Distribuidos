# Tarea 1 de Sistemas Distribuidos

## Distribución de carpetas:
Cada carpeta contiene el sistema de caché correspondiente (si es que aplica) y el search.py para poder realizar consultas.
### Carpeta cache_casero: 
En esta carpeta se encuentra el sistema que hace uso del caché casero.
### Carpeta no_cache: 
Esta carpeta solo incluye el search.py con lo necesario para funcionar, puesto que solo realiza la búsqueda en el JSON, sin utilizar algún sistema de caché.
### Carpeta memcached:
Aquí se encuentra también solo el search.py con lo necesario para funcionar, puesto que el sistema caché ya vienen implementado y solo se deben realizar las consultas.

## Levantamiento de contenedores.
Para levantar los contenedores:
1. Ingresar a la carpeta del sistema a levantar.
2. Ejecutar en la terminal: ``` sudo docker compose up -d ```
3. Ejecutar en la terminal: 
``` sudo docker exec -it search ``` (Para caché casero)
``` sudo docker exec -it search_mc ``` (Para memcached)
``` sudo docker exec -it search_no_cache ``` (Para no caché)
4. Una vez dentro del contenedor, ejecutar: ``` python3 search.py ``` 