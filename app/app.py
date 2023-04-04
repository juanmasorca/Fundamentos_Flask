from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# Conexion MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456789'
app.config['MYSQL_DB'] = 'api_flask'

conexion = MySQL(app)


@app.before_request
def before_request():
    print("Antes de la peticion")


@app.after_request
def after_request(response):
    print("Despues de la peticion")
    return response


@app.route('/')
def index():
    # return "abc"
    cursos = ['PHP', 'JAVA', 'PYTHON', 'CSS', 'HTML']
    data = {'titulo': 'Index123',
            'bienvenida': '¡Saludos!',
            'cursos': cursos,
            'numero_de_cursos': len(cursos),
            'total': 8}
    return render_template('index.html', data=data)


@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data = {'titulo': 'Contacto',
            'nombre': nombre,
            'edad': edad}
    return render_template('contacto.html', data=data)

# http://127.0.0.1:5000//query_string?param1=Juan&param2=24


def query_string():
    print(request)
    print(request.args)
    print(request.args.get('param1'))
    print(request.args.get('param2'))
    return 'ok'


@app.route('/cursos')
def listar_cursos():
    data = {}
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM curso ORDER BY Codigo ASC"
        cursor.execute(sql)
        # OBTENER DATOS
        cursos = cursor.fetchall()
        data['Cursos'] = cursos
        data['Mensaje'] = 'Exito'
    except Exception as ex:
        data['Mensaje'] = 'Error'
    return jsonify(data)


def pagina_no_encontrada(error):
    # return render_template('404.html'), 404
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug=True, port=5000)
