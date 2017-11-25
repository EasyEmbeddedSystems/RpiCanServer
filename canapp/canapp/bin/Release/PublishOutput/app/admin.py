from django.contrib import admin

from .models import Mensaje



#Permite ver objetos Mensajes con informacion entendible
class MensajeAdmin(admin.ModelAdmin):
	""" Permite acomodar y desplegar mejor la informacion para administrar Mensahes"""
	"""
	fieldsets = [
	("Tiempo transaccion", {'fields': ['transaccion_tiempo']}),
	('ID', {'fields': ['can_arbitration_id']}),
	('Dato', {'fields': ['can_data']}),
	]
	"""
	list_display = ("transaccion_modo", 'transaccion_tiempo', 'can_arbitration_id', 'can_data', "can_extended_id", "can_is_error_frame")


#Permite ver los objetos Mensajes de la base de datos
admin.site.register(Mensaje, MensajeAdmin)
