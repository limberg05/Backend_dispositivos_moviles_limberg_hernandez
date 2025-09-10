from flask import Blueprint,request,jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from config.db import get_db_connection, mysql

tareas_bp = Blueprint('tareas', __name__)

#crear endpoint
@tareas_bp.route('/obtener',methods=['GET'])
@jwt_required()
def get():
   current_user = get_jwt_identity()
   cursor = get_db_connection()
   
   query = '''
               SELECT a.id_usuario, a.descripcion, b.nombre, b.email, a.creado_en
               FROM tareas as a
               INNER JOIN usuarios as b on a.id_usuario = b.id_usuario
               WHERE a.id_usuario = %s
   '''
   cursor.execute(query,(current_user,))
   lista = cursor.fetchall()
   cursor.close()
   
   if not lista:
      return jsonify({"error":"el usuario no tiene tareas"}),404
   else:
      return jsonify({"lista":lista}),200

@tareas_bp.route('/crear', methods=['POST'])
@jwt_required()
def crear():
   # Obtener los datos del body
   current_user = get_jwt_identity()
   data = request.get_json()

   descripcion = data.get('descripcion')

   if not descripcion:
      return jsonify({"error": "Debes teclear una descripcion"}), 400

   # Obtenemos el cursor
   cursor = get_db_connection()

   # Hacemos el insert
   try:
      cursor.execute(
         'INSERT INTO tareas (descripcion, id_usuario) values (%s,%s)', (descripcion,current_user,))
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

@tareas_bp.route('/actualizar/<int:id_tarea>',methods=['PUT'])
@jwt_required()
def modificar(id_tarea):
   cursor = get_db_connection
   current_user = get_jwt_identity()
   
   
   data = request.get_json()
   descripcion =data.get('descripcion')
   
   query = '''
   SELECET * FROM tareas WHERE id_tarea = %s
   '''
   cursor.execute(query(id_tarea,))
   tarea = cursor.fetchone()
   
   if not tarea:
      return jsonify({"error":"esa tarea no existe"}),404
   
   if not tarea[1] == int(current_user):
      cursor.close()
      return jsonify({"error":"credenciales incorrectas"}),401
   
   try:
      cursor.execute("UPDATE tareas SET descripcion = %s WHERE id_tarea = %s", (descripcion,id_tarea))
      cursor.connection.commit()
      return jsonify ({"mensaje":"datos actualizados correctamente"})
   except Exception as e:
      return jsonify ({"error":"error al actualizar los datos:{str(e)}"})
      
   finally:
      cursor.close()