import pywhatkit as pwk
import time
from datetime import datetime, timedelta
import json

def load_messages():
    """Load messages and recipients from a JSON file."""
    try:
        with open('messages.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "messages": [
                "¡Hola! prueba de boot No.4",
                "prueba de boot",
                "Para whatsapp."
            ],
            "recipients": [
                "+52 1 414 219 5595" 
            ]
        }

def send_scheduled_message(phone_number, message):
    """
    Envía un mensaje programado a WhatsApp con delays apropiados
    para evitar el spam y respetar límites de uso.
    """
    try:
        now = datetime.now()        
        send_time = now + timedelta(minutes=1)
        
        print(f"Programando mensaje para {phone_number} a las {send_time.strftime('%H:%M')}")
        
        pwk.sendwhatmsg(
            phone_no=phone_number,
            message=message,
            time_hour=send_time.hour,
            time_min=send_time.minute,
            wait_time=20,
            tab_close=True
        )
        
        # tiempo de espera entre mensajes
        time.sleep(30)
        return True
        
    except Exception as e:
        print(f"Error al enviar mensaje: {str(e)}")
        return False

def main():
    
    config = load_messages()
    
    print("Iniciando envío de mensajes...")
    print(f"Número de destinatarios: {len(config['recipients'])}")
    
    for phone in config['recipients']:
        for message in config['messages']:
            success = send_scheduled_message(phone, message)
            
            if success:
                print(f"Mensaje enviado exitosamente a {phone}")
            else:
                print(f"Error al enviar mensaje a {phone}")
            
            time.sleep(10)

if __name__ == "__main__":
    print("""
    Hola este es mi boot de prueba jeje
    """)
    
    time.sleep(5)
    main()