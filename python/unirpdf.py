import PyPDF2

archivos = []
while True:
    nombre_archivo = input("Ingrese el nombre del archivo PDF (o escriba 'fin' para terminar): ")
    if nombre_archivo.lower() == "fin":
        break
    archivos.append(nombre_archivo)

nombre_salida = input("Ingrese el nombre del archivo de salida para el PDF unido: ")

pdf_final = PyPDF2.PdfMerger()
for nombre_archivo in archivos:
    pdf_final.append(nombre_archivo)

pdf_final.write(nombre_salida)
pdf_final.close()

print("Se ha creado el PDF unido:", nombre_salida)
