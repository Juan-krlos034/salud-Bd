from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import CitaCreateSerializer
from .services import (
    sp_agendar_cita, sp_cita_list_paciente, sp_cita_list_medico,
    sp_cita_cancel, sp_cita_list_all, sp_agenda_disponibilidad
)

class CitaViewSet(viewsets.ViewSet):
    
    def list(self, request):
        """Listar todas las citas"""
        data = sp_cita_list_all()
        return Response(data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Crear/Agendar una nueva cita"""
        serializer = CitaCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            nuevo_id = sp_agendar_cita(**serializer.validated_data)
            return Response(
                {
                    "id_cita": nuevo_id, 
                    "mensaje": "Cita agendada exitosamente"
                }, 
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(
                {"detail": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": f"Error al crear cita: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='paciente/(?P<id_paciente>[^/.]+)')
    def citas_paciente(self, request, id_paciente=None):
        """Obtener citas de un paciente"""
        data = sp_cita_list_paciente(int(id_paciente))
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='medico/(?P<id_medico>[^/.]+)')
    def citas_medico(self, request, id_medico=None):
        """Obtener citas de un médico"""
        data = sp_cita_list_medico(int(id_medico))
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='cancelar')
    def cancelar(self, request, pk=None):
        """Cancelar una cita"""
        filas = sp_cita_cancel(int(pk))
        if filas == 0:
            return Response(
                {"detail": "Cita no encontrada"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            {"mensaje": "Cita cancelada exitosamente"}, 
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='disponibilidad/(?P<id_medico>[^/.]+)')
    def disponibilidad(self, request, id_medico=None):
        """Obtener disponibilidad de un médico"""
        data = sp_agenda_disponibilidad(int(id_medico))
        return Response(data, status=status.HTTP_200_OK)