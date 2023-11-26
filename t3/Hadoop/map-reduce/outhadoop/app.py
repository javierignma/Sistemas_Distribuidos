from flask import Flask, render_template, request
from db import inicializar_base_datos
import wikipediaapi as wp

Wiki_object = wp.Wikipedia('Tarea3SD (javier.molina@mail.udp.cl)', 'es')

# Inicializar la base de datos
base_datos = inicializar_base_datos()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = None

    if request.method == 'POST':
        consulta = request.form['consulta']
        if consulta:
            # Realizar la búsqueda en la base de datos
            if consulta.lower() not in base_datos:
                resultados = [] 
            else:
                resultados = base_datos.get(consulta.lower())
                resultados = sorted(resultados, key=lambda x: int(x[1]), reverse=True)
                for doc in resultados:
                    doc.append(Wiki_object.page(doc[0]).fullurl)
                print(resultados)

    return render_template('index.html', consulta=request.form.get('consulta', ''), resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
