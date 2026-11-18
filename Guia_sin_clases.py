from datetime import date

ARCHIVO_LIBROS = "libros.txt"
ARCHIVO_PRESTAMOS = "prestamos.txt"

LIBROS_INICIALES = [
    {"codigo": 1, "titulo": "Python para todos", "autor": "Charles Severance", "estado": "Disponible"},
    {"codigo": 2, "titulo": "Aprende Java", "autor": "Ana Torres", "estado": "Disponible"},
    {"codigo": 3, "titulo": "Bases de datos", "autor": "Carlos Mora", "estado": "Disponible"},
]

def guardar_libros(libros):
    with open(ARCHIVO_LIBROS, "w", encoding="utf-8") as archivo:
        for libro in libros:
            linea = f"{libro['codigo']},{libro['titulo']},{libro['autor']},{libro['estado']}\n"
            archivo.write(linea)

def cargar_libros():
    libros = []
    try:
        with open(ARCHIVO_LIBROS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                libros.append({
                    "codigo": int(datos[0]),
                    "titulo": datos[1],
                    "autor": datos[2],
                    "estado": datos[3]
                })
    except FileNotFoundError:
        print("No se encontro libros.txt: se usan los libros iniciales.")
        for libro in LIBROS_INICIALES:
            libros.append(dict(libro))
        guardar_libros(libros)
    return libros

def guardar_prestamos(prestamos):
    with open(ARCHIVO_PRESTAMOS, "w", encoding="utf-8") as archivo:
        for prestamo in prestamos:
            linea = f"{prestamo['numero']},{prestamo['codigo_libro']},{prestamo['estudiante']},{prestamo['fecha']},{prestamo['estado']}\n"
            archivo.write(linea)

def cargar_prestamos():
    prestamos = []
    try:
        with open(ARCHIVO_PRESTAMOS, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                prestamos.append({
                    "numero": int(datos[0]),
                    "codigo_libro": int(datos[1]),
                    "estudiante": datos[2],
                    "fecha": datos[3],
                    "estado": datos[4]
                })
    except FileNotFoundError:
        print("No se encontro prestamos.txt: se inicia con lista vacia.")
    return prestamos

def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Error: debe escribir un numero entero.")

def leer_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            print("Error: el texto no puede estar vacio.")
        elif "," in texto:
            print("Error: el texto no puede contener comas.")
        else:
            return texto

def buscar_por_codigo(libros, codigo):
    for libro in libros:
        if libro["codigo"] == codigo:
            return libro
    return None

def registrar_libro(libros):
    print("\n--- REGISTRAR LIBRO ---")
    titulo = leer_texto("Titulo del libro: ")
    autor = leer_texto("Autor del libro: ")
    
    mayor_codigo = 0
    for libro in libros:
        if libro["codigo"] > mayor_codigo:
            mayor_codigo = libro["codigo"]
            
    nuevo_libro = {
        "codigo": mayor_codigo + 1,
        "titulo": titulo,
        "autor": autor,
        "estado": "Disponible"
    }
    libros.append(nuevo_libro)
    guardar_libros(libros)
    print(f"Libro registrado con exito. Codigo asignado: {nuevo_libro['codigo']}")
    return nuevo_libro

def mostrar_libros(libros):
    print("\n--- CATALOGO DE LIBROS ---")
    print(f"{'CODIGO':<8} {'TITULO':<30} {'AUTOR':<22} {'ESTADO':<12}")
    print("-" * 75)
    for libro in libros:
        print(f"{libro['codigo']:<8} {libro['titulo']:<30} {libro['autor']:<22} {libro['estado']:<12}")
    print("-" * 75)
    return len(libros)

def buscar_libro(libros):
    print("\n--- BUSCAR LIBRO ---")
    palabra = leer_texto("Ingrese palabra clave del titulo: ").lower()
    encontrados = 0
    print(f"\n{'CODIGO':<8} {'TITULO':<30} {'AUTOR':<22} {'ESTADO':<12}")
    print("-" * 75)
    for libro in libros:
        if palabra in libro["titulo"].lower():
            print(f"{libro['codigo']:<8} {libro['titulo']:<30} {libro['autor']:<22} {libro['estado']:<12}")
            encontrados += 1
    if encontrados == 0:
        print("No se encontraron libros con esa palabra.")
    return encontrados

def prestar_libro(libros, prestamos):
    print("\n--- PRESTAR LIBRO ---")
    codigo = leer_entero("Ingrese el codigo del libro a prestar: ")
    libro = buscar_por_codigo(libros, codigo)
    
    if libro is None:
        print("Error: no existe un libro con ese codigo.")
        return False
    if libro["estado"] != "Disponible":
        print("Error: el libro ya se encuentra prestado.")
        return False
        
    estudiante = leer_texto("Nombre del estudiante: ")
    numero_prestamo = len(prestamos) + 1
    nuevo_prestamo = {
        "numero": numero_prestamo,
        "codigo_libro": codigo,
        "estudiante": estudiante,
        "fecha": str(date.today()),
        "estado": "Activo"
    }
    
    prestamos.append(nuevo_prestamo)
    libro["estado"] = "Prestado"
    guardar_libros(libros)
    guardar_prestamos(prestamos)
    print(f"Prestamo #{numero_prestamo} registrado con exito.")
    return True

def devolver_libro(libros, prestamos):
    print("\n--- DEVOLVER LIBRO ---")
    codigo = leer_entero("Ingrese el codigo del libro a devolver: ")
    libro = buscar_por_codigo(libros, codigo)
    
    if libro is None:
        print("Error: no existe un libro con ese codigo.")
        return False
    if libro["estado"] != "Prestado":
        print("Error: ese libro no esta prestado actualmente.")
        return False
        
    libro["estado"] = "Disponible"
    for prestamo in prestamos:
        if prestamo["codigo_libro"] == codigo and prestamo["estado"] == "Activo":
            prestamo["estado"] = "Devuelto"
            break
            
    guardar_libros(libros)
    guardar_prestamos(prestamos)
    print("Devolucion registrada con exito.")
    return True

def mostrar_prestamos(prestamos, libros):
    print("\n--- LISTA DE PRESTAMOS ---")
    if len(prestamos) == 0:
        print("No hay prestamos registrados.")
        return 0
        
    print(f"{'NRO':<6} {'COD. LIBRO':<12} {'TITULO':<24} {'ESTUDIANTE':<18} {'FECHA':<12} {'ESTADO':<10}")
    print("-" * 92)
    for prestamo in prestamos:
        libro = buscar_por_codigo(libros, prestamo["codigo_libro"])
        titulo = libro["titulo"] if libro is not None else "Desconocido"
        print(f"{prestamo['numero']:<6} {prestamo['codigo_libro']:<12} {titulo:<24} {prestamo['estudiante']:<18} {prestamo['fecha']:<12} {prestamo['estado']:<10}")
    print("-" * 92)
    return len(prestamos)

def reporte_general(libros, prestamos):
    print("\n--- REPORTE GENERAL ---")
    disponibles = 0
    prestados = 0
    for libro in libros:
        if libro["estado"] == "Disponible":
            disponibles += 1
        elif libro["estado"] == "Prestado":
            prestados += 1
            
    activos = 0
    for prestamo in prestamos:
        if prestamo["estado"] == "Activo":
            activos += 1
            
    total_libros = len(libros)
    try:
        porcentaje = (prestados / total_libros) * 100
    except ZeroDivisionError:
        porcentaje = 0.0
        
    print(f"Total de libros: {total_libros}")
    print(f"Libros disponibles: {disponibles}")
    print(f"Libros prestados: {prestados}")
    print(f"Total prestamos registrados: {len(prestamos)}")
    print(f"Prestamos activos: {activos}")
    print(f"Porcentaje de libros prestados: {porcentaje:.1f} %")
    return porcentaje

def main():
    libros = cargar_libros()
    prestamos = cargar_prestamos()
    opcion = 0
    while opcion != 8:
        print("""
==================================
    BIBLIOTECA DIGITAL TEC AZUAY
==================================
1. Registrar libro
2. Mostrar libros
3. Buscar libro
4. Prestar libro
5. Devolver libro
6. Mostrar prestamos
7. Reporte general
8. Salir""")
        opcion = leer_entero("Elija una opcion: ")
        if opcion == 1:
            registrar_libro(libros)
        elif opcion == 2:
            mostrar_libros(libros)
        elif opcion == 3:
            buscar_libro(libros)
        elif opcion == 4:
            mostrar_libros(libros)
            prestar_libro(libros, prestamos)
        elif opcion == 5:
            mostrar_prestamos(prestamos, libros)
            devolver_libro(libros, prestamos)
        elif opcion == 6:
            mostrar_prestamos(prestamos, libros)
        elif opcion == 7:
            reporte_general(libros, prestamos)
        elif opcion == 8:
            guardar_libros(libros)
            guardar_prestamos(prestamos)
            print("Datos guardados. Hasta pronto!")
        else:
            print("Opcion no valida: elija un numero del 1 al 8.")

if __name__ == "__main__":
    main()