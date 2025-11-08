from django.db import connection

# ===== AGENDAR CITA (usando tu SP) =====
def sp_agendar_cita(id_paciente, id_agenda, estado='Programada'):
    with connection.cursor() as cursor:
        cursor.execute(
            "CALL sp_agendar_cita(%s, %s, %s)",
            [id_paciente, id_agenda, estado]
        )
        row = cursor.fetchone()
        # Verificar si es error o éxito
        mensaje = row[0] if row else None
        if mensaje and 'Error' in mensaje:
            raise ValueError(mensaje)
        
        # Si hay más columnas, es éxito
        id_cita = row[1] if len(row) > 1 else None
        return id_cita

# ===== LISTAR CITAS DE PACIENTE =====
def sp_cita_list_paciente(id_paciente):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                c.ID_Cita,
                c.Estado,
                c.ID_Paciente,
                c.ID_Medico,
                CONCAT(u.Nombre, ' ', u.Apellidos) as medico_nombre,
                a.Fecha,
                a.Hora
            FROM Cita c
            INNER JOIN Medico m ON c.ID_Medico = m.ID_Medico
            INNER JOIN Usuario u ON m.ID_Usuario = u.ID_Usuario
            INNER JOIN Agenda a ON c.ID_Agenda = a.ID_Agenda
            WHERE c.ID_Paciente = %s
            ORDER BY a.Fecha DESC, a.Hora DESC
            """,
            [id_paciente]
        )
        rows = cursor.fetchall()
        return [
            {
                "id_cita": r[0],
                "estado": r[1],
                "id_paciente": r[2],
                "id_medico": r[3],
                "medico_nombre": r[4],
                "fecha": str(r[5]),
                "hora": str(r[6]),
            } for r in rows
        ]

# ===== LISTAR CITAS DE MÉDICO =====
def sp_cita_list_medico(id_medico):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                c.ID_Cita,
                c.Estado,
                c.ID_Paciente,
                CONCAT(u.Nombre, ' ', u.Apellidos) as paciente_nombre,
                a.Fecha,
                a.Hora
            FROM Cita c
            INNER JOIN Paciente p ON c.ID_Paciente = p.ID_Paciente
            INNER JOIN Usuario u ON p.ID_Usuario = u.ID_Usuario
            INNER JOIN Agenda a ON c.ID_Agenda = a.ID_Agenda
            WHERE c.ID_Medico = %s
            ORDER BY a.Fecha DESC, a.Hora DESC
            """,
            [id_medico]
        )
        rows = cursor.fetchall()
        return [
            {
                "id_cita": r[0],
                "estado": r[1],
                "id_paciente": r[2],
                "paciente_nombre": r[3],
                "fecha": str(r[4]),
                "hora": str(r[5])
            } for r in rows
        ]

# ===== CANCELAR CITA =====
def sp_cita_cancel(id_cita):
    with connection.cursor() as cursor:
        cursor.execute(
            "UPDATE Cita SET Estado = 'Cancelada' WHERE ID_Cita = %s",
            [id_cita]
        )
        return cursor.rowcount

# ===== LISTAR TODAS LAS CITAS =====
def sp_cita_list_all():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                c.ID_Cita,
                c.Estado,
                c.ID_Paciente,
                c.ID_Medico,
                a.Fecha,
                a.Hora
            FROM Cita c
            INNER JOIN Agenda a ON c.ID_Agenda = a.ID_Agenda
            ORDER BY a.Fecha DESC, a.Hora DESC
            """
        )
        rows = cursor.fetchall()
        return [
            {
                "id_cita": r[0],
                "estado": r[1],
                "id_paciente": r[2],
                "id_medico": r[3],
                "fecha": str(r[4]),
                "hora": str(r[5])
            } for r in rows
        ]

# ===== DISPONIBILIDAD DE MÉDICO =====
def sp_agenda_disponibilidad(id_medico):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT 
                ID_Agenda,
                Fecha,
                Hora,
                Disponible
            FROM Agenda
            WHERE ID_Medico = %s
            AND Disponible = TRUE
            AND Fecha >= CURDATE()
            ORDER BY Fecha ASC, Hora ASC
            """,
            [id_medico]
        )
        rows = cursor.fetchall()
        return [
            {
                "id_agenda": r[0],
                "fecha": str(r[1]),
                "hora": str(r[2]),
                "disponible": bool(r[3])
            } for r in rows
        ]