"""
Definition of views.
"""

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from app.models import Mensaje
from django.utils import timezone
import app.models as MODEL
import can

can.rc['interface'] = 'socketcan_ctypes'
#can.rc['interface'] = 'virtual'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 125000
bus =  can.interface.Bus()

def home(request):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	return render(
        request,
        'app/index.html',
        {
            'title':'Servidor CAN',
            'year':datetime.now().year,
            'mensajes_enviados': Mensaje.objects.filter(transaccion_modo=MODEL.ENVIAR).order_by('-pk')[:10]
        },
		
    )


def recibir(request):
	"""Renders the home page."""
	assert isinstance(request, HttpRequest)
	return render(
        request,
        'app/recibir.html',
        {
            'title':'Servidor CAN',
            'year':datetime.now().year,
			'mensajes_recibidos': Mensaje.objects.filter(transaccion_modo=MODEL.RECIBIR).order_by('-pk')[:20]
        },
		
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contacto',
            'message':'Creado por Wilbert Caballero.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'Acerca de',
            'message':'Servidor CAN. Proyecto de la clase Redes Automotrices MSC UAQ. Utiliza Python-CAN, Django, MCP2515 y Raspberry PI.',
            'year':datetime.now().year,
        }
    )



def validar_arbitration_id(can_arbitration_id):
    '''
    Valida que el valor del ID sea válido:
    covierte el ID string a int y valida que su valor sea mayor a cero.
    255 -> "FF"
    '''
    result = False
    try:
        valor = int(can_arbitration_id,16)
        if(valor > 0):
            result=True
    except :
        result = False
    return result

def validar_dato(can_data):
    '''
    Valida que el dato tenga el formato adecuado:
    Un byte en string hexadecimal compuesto por dos nibbles.
    255 -> "FF"
    '''
    result = False
    longitud =len(can_data)
    if(longitud>0):
        if(longitud%2==0):
            result=True
    return result


def mandar_dato(can_arbitration_id, can_data):
    '''
    Manda  el mensaje por la libreria python-can
    Guarda el mensaje en el modelo actual (base de datos).
    '''
    sent_mes_error = False;
    can_msj = can.Message(
                arbitration_id=int(can_arbitration_id,16),
			    data=can_data,			    
            )   
    try:
        bus.send(can_msj)
        print('Mensaje enviado en {}'.format(bus.channel_info))
        sent_mes_error = False
    except can.CanError:
        print('Mensaje No envaido')
        sent_mes_error = True
    finally:
        model_msj = Mensaje(
            transaccion_modo = MODEL.ENVIAR,
			transaccion_tiempo = timezone.now(),
			can_data = ''.join('{:02X}'.format(x) for x in can_data),
			can_arbitration_id = can_arbitration_id,
            can_is_error_frame = sent_mes_error,
			)
        model_msj.save()
               

def decode(data):
    '''
    Decodificar el dato para transformalo a un arreglo de bytes tal como se utiliza en la libreria python-can
    '''
    return bytearray.fromhex(data)

def enviar(request):
    '''
    Procesa la petición POST generada por el acceso URL.
    Verificar que se trate de un servicio POST.
    Verificar el ID y el Dato.
    Si verificaciones son correctas, Manda el Mensaje.
    '''
    if(request.POST):
        print('** Enviando POST', request)
        can_arbitration_id = request.POST["arbitration_id"]
        can_data = request.POST["data"]
        if validar_arbitration_id(can_arbitration_id):
            print("ID válido %s" %(can_arbitration_id))
            if validar_dato(can_data):
                print ("Dato válido %s" %(can_data))
                #enviar dato y guardar
                mandar_dato(can_arbitration_id, decode(can_data))
                # Popup con mensaje enviado.
                messages.add_message(request, messages.SUCCESS, 'Mensaje enviado.')			    
            else:
                # Popup con error de mensaje (dato)
                messages.add_message(request, messages.ERROR, 'Dato invalido, debe ser multiplos de 2.')
                print('ERROR DATO')
        else:
            # Popup con error de mensaje (ID)
            messages.add_message(request, messages.ERROR, 'ID invalido, debe ser mayor a cero.')
            print('ERROR ID')    
        #Regresa a la misma página con el listado más reciente de mensajes enviado.
        return HttpResponseRedirect('app/index.html', { 'mensajes_enviados': Mensaje.objects.filter(transaccion_modo=MODEL.ENVIAR).order_by('-pk')[:10]})    
    else:
        print('** Enviar GET', request)
        #Regresa a la misma página con el listado más reciente de mensajes enviado.
        return render(request, 'app/index.html', { 'mensajes_enviados': Mensaje.objects.filter(transaccion_modo=MODEL.ENVIAR).order_by('-pk')[:10]})


class CanListener(can.Listener):
    '''
    Manejador de evento de recepción de datos por medio de python-can
    Se sobrescribe el metodo "on_message_received"
    y se guarda un mensaje modelo con la información de mensaje de can.
    '''
    def on_message_received(self, msj):
        print(msj)
        model_msj = Mensaje(
				transaccion_tiempo = timezone.now(),
				transaccion_modo = MODEL.RECIBIR,
				can_timestamp = msj.timestamp,
				can_is_remote_frame = msj.is_remote_frame,
				can_extended_id = msj.is_extended_id,
				can_is_error_frame = msj.is_error_frame,
				#can_arbitration_id = hex(msj.arbitration_id),
				can_arbitration_id = format(msj.arbitration_id,'x'),
				can_dlc = msj.dlc,
				can_data =  ''.join('{:02X}'.format(x) for x in  msj.data)
				)
        model_msj.save()

#Crear un nuevo objeto con el manejador de recpción de datos can.
can_listener = CanListener()

#Agregar el manejador apenas creado al notificador de eventos del bus de can.
susucribirse_notificaciones = can.Notifier(bus, [can_listener])
