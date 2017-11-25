"""
Definition of models.
"""

from django.db import models

# Create your models here.
import can

ENVIAR = 'ENVIAR'
RECIBIR = 'RECIBIR'
MODO_OPCIONES = (
    (ENVIAR, 'Envio'),
    (RECIBIR, 'Recepcion'),
)

class Mensaje(models.Model):		
	transaccion_tiempo = models.DateTimeField('Tiempo de transaccion' )
	transaccion_modo = models.CharField('Modo de transaccion', max_length=200, choices=MODO_OPCIONES)
	can_timestamp = models.FloatField('CAN - Marcaje de Tiempo', null=True)
	can_is_remote_frame = models.BooleanField('CAN - Frame Remoto', default=False)
	can_extended_id = models.BooleanField('CAN - ID Extendido', default=True)
	can_is_error_frame = models.BooleanField('CAN - Frame de Error', default=False)
	can_arbitration_id = models.CharField('CAN - ID Mensaje',max_length=10)
	can_dlc = models.IntegerField('CAN - DLC',  null=True)
	can_data = models.CharField('CAN - Dato', max_length=200)


	def __str__(self):
		return str(self.can_arbitration_id) + "#" + str(self.can_data)
