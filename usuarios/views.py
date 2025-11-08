from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password, check_password
from .serializers import UsuarioCreateUpdateSerializer, UsuarioSerializer
from .services import (
    sp_usuario_create, sp_usuario_get, sp_usuario_list,
    sp_usuario_update, sp_usuario_delete, sp_usuario_login,
    sp_usuario_reset_password, sp_usuario_buscar
)
from django.db import connection, DatabaseError


class UsuarioViewSet(viewsets.ViewSet):
    """
    Endpoints:
    - GET    /api/usuarios/        -> list
    - GET    /api/usuarios/{id}/   -> retrieve
    - POST   /api/usuarios/        -> create
    - PUT    /api/usuarios/{id}/   -> update
    - DELETE /api/usuarios/{id}/   -> destroy
    """

    def list(self, request):
        data = sp_usuario_list()
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        item = sp_usuario_get(int(pk))
        if not item:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(item, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = UsuarioCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        data["contrasena"] = make_password(data["contrasena"])
        
        try:
            nuevo_id = sp_usuario_create(**data)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError:
            return Response({"detail": "Error en la base de datos"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        item = sp_usuario_get(nuevo_id)
        return Response(item, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        serializer = UsuarioCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('rol', None)
        filas = sp_usuario_update(int(pk), **serializer.validated_data)
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        item = sp_usuario_get(int(pk))
        return Response(item, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk=None):
        filas = sp_usuario_delete(int(pk))
        if filas == 0:
            return Response({"detail": "No encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        correo = request.data.get("correo")
        contrasena = request.data.get("contrasena")

        if not correo or not contrasena:
            return Response(
                {"detail": "Correo y contraseña requeridos"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ID_Usuario, Nombre, Apellidos, Rol, Contrasena FROM Usuario WHERE Correo = %s",
                    [correo]
                )
                row = cursor.fetchone()
            
            if not row:
                return Response(
                    {"detail": "Credenciales inválidas"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not check_password(contrasena, row[4]):
                return Response(
                    {"detail": "Credenciales inválidas"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            user_data = {
                "id_usuario": row[0],
                "nombre": row[1],
                "apellidos": row[2],
                "rol": row[3],
                "correo": correo
            }
            
            return Response(user_data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"detail": f"Error en el servidor: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['post'], url_path='reset_password')
    def reset_password(self, request):
        correo = request.data.get("correo")
        nueva = request.data.get("nueva_contrasena")

        if not correo or not nueva:
            return Response(
                {"detail": "Correo y nueva contraseña requeridos"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        nueva_encriptada = make_password(nueva)
        filas = sp_usuario_reset_password(correo, nueva_encriptada)

        if filas == 0:
            return Response(
                {"detail": "Correo no encontrado"}, 
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"detail": "Contraseña actualizada correctamente"}, 
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='buscar')
    def buscar(self, request):
        q = request.query_params.get("q", "")
        if not q:
            return Response(
                {"detail": "Debe indicar un parámetro de búsqueda ?q="}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = sp_usuario_buscar(q)
        return Response(data, status=status.HTTP_200_OK)