import ast

def inicializar_base_datos():
    # Coloca aquí la lógica para inicializar la base de datos
    with open('part-00000', 'r') as file:
        lineas = file.readlines()

    base_datos = {}
    for linea in lineas:
        try:
            # Dividir la línea en palabra y documentos_str
            palabra, documentos_str = linea.strip().split('\t')

            # Convertir la cadena de documentos_str a una lista de tuplas
            documentos = [tuple(documento.strip('(),').split(',')) for documento in documentos_str.split(') (')]

            # Almacenar en la base de datos
            base_datos[palabra] = documentos
        except ValueError as e:
            print(f"Error al procesar la línea: {linea}")
            print(f"Error específico: {e}")

    return base_datos
