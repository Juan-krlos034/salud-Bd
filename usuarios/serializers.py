from rest_framework import serializers

class UsuarioCreateUpdateSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=100)
    documento = serializers.CharField(max_length=50)
    fecha_nacimiento = serializers.DateField(required=False)
    correo = serializers.EmailField()
    telefono = serializers.CharField(max_length=20, required=False)
    contrasena = serializers.CharField(max_length=100)
    rol = serializers.ChoiceField(choices=["Paciente", "Medico", "Administrador"])


class UsuarioSerializer(serializers.Serializer):
    id_usuario = serializers.IntegerField()
    nombre = serializers.CharField(max_length=100)
    apellidos = serializers.CharField(max_length=100)
    documento = serializers.CharField(max_length=50)
    correo = serializers.EmailField()
    telefono = serializers.CharField(max_length=20, allow_null=True)
    rol = serializers.CharField(max_length=20)
