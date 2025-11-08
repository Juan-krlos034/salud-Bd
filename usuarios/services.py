from django.db import connection, DatabaseError

# ✅ CREATE
def sp_usuario_create(nombre, apellidos, documento, fecha_nacimiento, correo, telefono, contrasena, rol):
    try:
        with connection.cursor() as cursor:
            cursor.execute("CALL sp_usuario_create(%s,%s,%s,%s,%s,%s,%s,%s)", 
                        [nombre, apellidos, documento, fecha_nacimiento, correo, telefono, contrasena, rol])
            row = cursor.fetchone()  # debe devolver LAST_INSERT_ID() o algo similar
            return int(row[0]) if row else None
    except DatabaseError as e:
        if "Duplicate" in str(e):
            raise ValueError("Documento o correo ya existe")
        raise e
        

# ✅ GET BY ID
def sp_usuario_get(uid: int):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_usuario_get(%s)", [uid])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_usuario": row[0],
            "nombre": row[1],
            "apellidos": row[2],
            "documento": row[3],
            "correo": row[4],
            "telefono": row[5],
            "rol": row[6],
        }

# ✅ LIST
def sp_usuario_list():
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_usuario_list()")
        rows = cursor.fetchall()
        return [
            {
                "id_usuario": r[0],
                "nombre": r[1],
                "apellidos": r[2],
                "documento": r[3],
                "correo": r[4],
                "telefono": r[5],
                "rol": r[6],
            } for r in rows
        ]

# ✅ UPDATE
def sp_usuario_update(
    id_usuario: int,
    nombre: str,
    apellidos: str,
    documento: str,
    fecha_nacimiento,
    correo: str,
    telefono: str,
    contrasena: str
) -> int:
    with connection.cursor() as cursor:
        cursor.callproc('sp_usuario_update', [
            id_usuario,
            nombre,
            apellidos,
            documento,
            fecha_nacimiento,
            correo,
            telefono,
            contrasena
        ])
        row = cursor.fetchone()
        return int(row[0]) if row else 0


# ✅ DELETE
def sp_usuario_delete(uid: int) -> int:
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_usuario_delete(%s)", [uid])
        row = cursor.fetchone()  # tu SP debe hacer SELECT ROW_COUNT()
        return int(row[0]) if row else 0

def sp_usuario_login(correo: str, contrasena: str):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_usuario_login(%s, %s)", [correo, contrasena])
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id_usuario": row[0],
            "nombre": row[1],
            "apellidos": row[2],
            "rol": row[3],
        }
def sp_usuario_reset_password(correo: str, nueva_contrasena: str):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_usuario_reset_password(%s, %s)", [correo, nueva_contrasena])
        row = cursor.fetchone()
        return int(row[0]) if row else 0

def sp_usuario_buscar(texto: str):
    with connection.cursor() as cursor:
        cursor.execute("CALL sp_usuario_buscar(%s)", [texto])
        rows = cursor.fetchall()
        return [
            {
                "id_usuario": r[0],
                "nombre": r[1],
                "apellidos": r[2],
                "correo": r[3],
                "rol": r[4],
            } for r in rows
        ]
