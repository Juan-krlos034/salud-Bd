from rest_framework import serializers

class CitaCreateSerializer(serializers.Serializer):
    id_paciente = serializers.IntegerField()
    id_agenda = serializers.IntegerField()
    estado = serializers.CharField(max_length=20, default='Programada')

class CitaSerializer(serializers.Serializer):
    id_cita = serializers.IntegerField()
    estado = serializers.CharField()
    id_paciente = serializers.IntegerField()
    id_medico = serializers.IntegerField()
    fecha = serializers.CharField()
    hora = serializers.CharField()