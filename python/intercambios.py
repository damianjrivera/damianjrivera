import random

def intercambio_regalos():
    participantes = []
    
    print("INTERCAMBIO MAMALONSOTE EN CASA DEL MIGUELON")
    
    while True:
        nombre = input("Nombre del participante ").strip()
        if nombre == "":
            break
        participantes.append(nombre)

    if len(participantes) < 3:
        print("Deben ser al menos 3 participantes para hacer el intercambio.")
        return
    destinatarios = participantes.copy()
    emparejamientos = {}
    
    for persona in participantes:
        posibles_destinatarios = [d for d in destinatarios if d != persona]
        
        if not posibles_destinatarios:
            print("No se puede realizar el intercambio. Intenta de nuevo.")
            return
        destinatario = random.choice(posibles_destinatarios)

        emparejamientos[persona] = destinatario
        
        destinatarios.remove(destinatario)
    print("\n--- Emparejamientos de Intercambio mamalon ---")
    for persona, destinatario in emparejamientos.items():
        confirmacion = input(f"{persona} va a regalar a... (Presiona 'S'").upper()
        if confirmacion == 'S':
            print(f"{persona} le regala a {destinatario}\n")
        else:
            print("Revelación cancelada.\n")

if __name__ == "__main__":
    intercambio_regalos()