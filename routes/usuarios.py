from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt
from flask_bcrypt import Bcrypt

from config.db import get_db_connection

import os
from dotenv import load_dotenv


load_dotenv()

usuarios_bp = Blueprint('usuarios', __name__)


bcrypt = Bcrypt()

@usuarios_bp.route('/registrar', methods=['POST'])
def registrar():
    data = request.get_json()
    
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    
    if not nombre or not email or not password:
        return jsonify({"error":"Falta info"}),400
    
    cursor = get_db_connection()
    
    try:
        cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return jsonify({"error":"ese user ya existe"}),400
    
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        cursor.execute('''INSERT INTO usuarios (nombre, email, password) values (%s,%s,%s)''',(nombre,email,hashed_password))
    
        cursor.connection.commit()
        return jsonify({"succesfull":f"no hubo error al registrar al usuario"}),200


    except Exception as e:
        return jsonify({"error":f"Error al registrar al usuario:{str(e)}"}),500
    
    finally:
        cursor.close()