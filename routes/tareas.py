from flask import Blueprint,request,jsonify
from config.db import get_db_connection, mysql

tareas_bp = Blueprint('tareas', __name__)

#crear endpoint
@tareas_bp.route('/obtener',methods=['GET'])
def get():
   return jsonify({"mensaje":"estas son tus tareas"})


@tareas_bp.route('/crear', methods=['POST'])
def crear():
   # Obtener los datos del body

   data = request.get_json()

   descripcion = data.get('descripcion')

   if not descripcion:
      return jsonify({"error": "Debes teclear una descripcion"}), 400

   # Obtenemos el cursor
   cursor = get_db_connection()

   # Hacemos el insert
   try:
      cursor.execute(
         'INSERT INTO tareas (descripcion) values (%s)', (descripcion,))
      cursor.connection.commit()
      return jsonify({"message": "Tarea creada"}), 201
   except Exception as e:
      return jsonify({"Error": f"No se pudo crear la tarea: {str(e)}"})
   finally:
      cursor.close()
   
   
   
@tareas_bp.route('/actualizar/<int:user_id>',methods=['PUT'])
def put(user_id):
   data = request.get_json()
   nombre =data.get('nombre')
   apellido =data.get('apellido')
   mensaje = f"usuario con id:{user_id} y nombre: {nombre} {apellido}"
   return jsonify({"saludo":mensaje})
