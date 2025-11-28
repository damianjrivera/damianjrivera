# traductor de java a python prueba 3
def traducir_java_a_python(codigo_java):
    codigo_completo = ""

    while True:
        if codigo_java.strip() == "0204":  
            break
        codigo_completo += codigo_java + "\n"  
        codigo_java = input()  # Leer siguiente línea

    #diccionario de equivalencias de palabras clave y constructores
    equivalencias = {
        'public': '',
        'class': 'class',
        'static': '@staticmethod',
        'void': 'def',
        'int': 'int',
        'double': 'float',
        'String': 'str',
        'if': 'if',
        'else': 'else',
        'for': 'for',
        'while': 'while',
        'return': 'return',
        'true': 'True',
        'false': 'False'
     }

    # Reemplazar las palabras clave y constructores de Java con los equivalentes en Python
    for clave, valor in equivalencias.items():
        codigo_completo = codigo_completo.replace(clave + ' ', valor + ' ')

    # Reemplazar algunos otros elementos específicos de Java
    codigo_python = codigo_completo.replace('System.out.println', 'print')

    return codigo_python

def traducir_java():
    print("Ingrese el código Java a traducir (Ingrese '0204' para terminar):")
    codigo_java = input()

    codigo_python = traducir_java_a_python(codigo_java)

    print("\nCódigo Python traducido:")
    print(codigo_python)

def main():
    traducir_java()

main()
