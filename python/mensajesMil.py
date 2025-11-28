from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

# Límite máximo de mensajes
MAX_MESSAGES = 10
messages_sent = 0

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
                "+52 1 442 338 5510"  # telefono a enviar
            ]
        }

def init_driver():
    """Inicializa el navegador Chrome."""
    print("Iniciando navegador...")
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')

    
    driver = webdriver.Chrome(options=options)
    driver.get('https://web.whatsapp.com')
    
    print("\n Por favor, escanea el código QR de WhatsApp Web...")
    print("Esperando 30 segundos para que inicies sesión...\n")
    time.sleep(30)  # Tiempo para escanear QR
    
    return driver

def send_message(driver, phone_number, message):
    """Envía un mensaje a través de WhatsApp Web usando Selenium."""
    global messages_sent
    
    if messages_sent >= MAX_MESSAGES:
        print(f"\n LÍMITE ALCANZADO: Se han enviado {messages_sent} mensajes.")
        return False
    
    try:

        phone_clean = phone_number.replace(" ", "").replace("+", "").replace("-", "")
        
        url = f'https://web.whatsapp.com/send?phone={phone_clean}'
        driver.get(url)
        
        wait = WebDriverWait(driver, 15)
        
        input_box = wait.until(EC.presence_of_element_located((
            By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'
        )))
        
        # Enviar el mensaje
        input_box.click()
        time.sleep(0.5)
        input_box.send_keys(message)
        time.sleep(0.5)
        input_box.send_keys(Keys.ENTER)
        
        messages_sent += 1
        print(f"✓ Mensaje {messages_sent}/{MAX_MESSAGES} enviado a {phone_number}")
        
        # Espera mínima entre mensajes
        time.sleep(1)
        return True
        
    except TimeoutException:
        print(f"✗ Timeout: No se pudo cargar el chat de {phone_number}")
        return False
    except NoSuchElementException:
        print(f"✗ Error: No se encontró el cuadro de texto para {phone_number}")
        return False
    except Exception as e:
        print(f"✗ Error al enviar mensaje a {phone_number}: {str(e)}")
        return False

def main():
    global messages_sent
    
    # Cargar configuración
    config = load_messages()
    
    print("=" * 60)
    print("Bot de WhatsApp con Límite de Mensajes (Selenium)")
    print(f"Límite configurado: {MAX_MESSAGES} mensajes")
    print("=" * 60)
    print(f"Número de destinatarios: {len(config['recipients'])}")
    print(f"Mensajes por destinatario: {len(config['messages'])}\n")
    
    # Inicializar navegador
    driver = init_driver()
    
    try:
        print("✓ Sesión iniciada. Comenzando envío de mensajes...\n")
        
        for phone in config['recipients']:
            if messages_sent >= MAX_MESSAGES:
                print(f"\n✓ Proceso finalizado. Total: {messages_sent} mensajes")
                break
            
            for message in config['messages']:
                if messages_sent >= MAX_MESSAGES:
                    print(f"\n✓ Proceso finalizado. Total: {messages_sent} mensajes")
                    break
                
                send_message(driver, phone, message)
                
        print(f"\n Programa completado. Mensajes enviados: {messages_sent}/{MAX_MESSAGES}")
        print("\nEl navegador se cerrará en 10 segundos...")
        time.sleep(10)
        
    except KeyboardInterrupt:
        print(f"\n\n Programa interrumpido por el usuario.")
        print(f"Mensajes enviados: {messages_sent}/{MAX_MESSAGES}")
    
    finally:
        driver.quit()
        print("Navegador cerrado.")

if __name__ == "__main__":
    main()