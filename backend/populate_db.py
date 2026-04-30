"""
Script para poblar la base de datos con supermercados de ejemplo en Chile.
Ejecutar: python populate_db.py
"""
from app.database import SessionLocal, engine
from app.models import Base, Supermercado
from datetime import datetime

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

def poblar_supermercados():
    db = SessionLocal()
    
    # Verificar si ya hay datos
    count = db.query(Supermercado).count()
    if count > 0:
        print(f"Ya existen {count} supermercados en la base de datos.")
        respuesta = input("¿Deseas agregar más supermercados? (s/n): ")
        if respuesta.lower() != 's':
            db.close()
            return
    
    # Supermercados de ejemplo en Santiago, Chile
    supermercados_ejemplo = [
        # Zona Centro/Providencia
        {
            "nombre": "Lider Providencia",
            "cadena": "Lider",
            "direccion": "Av. Providencia 2330",
            "comuna": "Providencia",
            "ciudad": "Santiago",
            "latitud": -33.4280,
            "longitud": -70.6108,
            "telefono": "+56 2 2950 0000",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Jumbo Bilbao",
            "cadena": "Jumbo",
            "direccion": "Av. Bilbao 1129",
            "comuna": "Providencia",
            "ciudad": "Santiago",
            "latitud": -33.4342,
            "longitud": -70.6137,
            "telefono": "+56 2 2630 5000",
            "horario": "Lun-Dom 8:30-22:00"
        },
        {
            "nombre": "Unimarc Alameda",
            "cadena": "Unimarc",
            "direccion": "Av. Libertador Bernardo O'Higgins 2912",
            "comuna": "Santiago",
            "ciudad": "Santiago",
            "latitud": -33.4489,
            "longitud": -70.6693,
            "telefono": "+56 2 2680 9000",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # Zona Oriente - Las Condes
        {
            "nombre": "Jumbo Kennedy",
            "cadena": "Jumbo",
            "direccion": "Av. Kennedy 9001",
            "comuna": "Las Condes",
            "ciudad": "Santiago",
            "latitud": -33.4088,
            "longitud": -70.5770,
            "telefono": "+56 2 2959 0000",
            "horario": "Lun-Dom 8:00-23:00"
        },
        {
            "nombre": "Lider Apumanque",
            "cadena": "Lider",
            "direccion": "Av. Manquehue Norte 1410",
            "comuna": "Las Condes",
            "ciudad": "Santiago",
            "latitud": -33.4100,
            "longitud": -70.5965,
            "telefono": "+56 2 2950 1000",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Las Condes",
            "cadena": "Santa Isabel",
            "direccion": "Av. Apoquindo 4900",
            "comuna": "Las Condes",
            "ciudad": "Santiago",
            "latitud": -33.4130,
            "longitud": -70.5890,
            "telefono": "+56 2 2425 8000",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # Zona Oriente - Vitacura
        {
            "nombre": "Jumbo Vitacura",
            "cadena": "Jumbo",
            "direccion": "Av. Vitacura 7140",
            "comuna": "Vitacura",
            "ciudad": "Santiago",
            "latitud": -33.3890,
            "longitud": -70.5680,
            "telefono": "+56 2 2959 2000",
            "horario": "Lun-Dom 8:00-23:00"
        },
        
        # Zona Sur - La Florida
        {
            "nombre": "Lider La Florida",
            "cadena": "Lider",
            "direccion": "Av. Vicuña Mackenna 6100",
            "comuna": "La Florida",
            "ciudad": "Santiago",
            "latitud": -33.5200,
            "longitud": -70.5950,
            "telefono": "+56 2 2950 3000",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Tottus La Florida",
            "cadena": "Tottus",
            "direccion": "Av. Walker Martínez 1351",
            "comuna": "La Florida",
            "ciudad": "Santiago",
            "latitud": -33.5280,
            "longitud": -70.6020,
            "telefono": "+56 2 2530 0000",
            "horario": "Lun-Dom 8:30-22:30"
        },
        
        # Zona Poniente - Maipú
        {
            "nombre": "Jumbo Maipú",
            "cadena": "Jumbo",
            "direccion": "Av. Américo Vespucio 1001",
            "comuna": "Maipú",
            "ciudad": "Santiago",
            "latitud": -33.5090,
            "longitud": -70.7580,
            "telefono": "+56 2 2959 4000",
            "horario": "Lun-Dom 8:00-23:00"
        },
        {
            "nombre": "Lider Maipú",
            "cadena": "Lider",
            "direccion": "Av. Pajaritos 2255",
            "comuna": "Maipú",
            "ciudad": "Santiago",
            "latitud": -33.5150,
            "longitud": -70.7720,
            "telefono": "+56 2 2950 5000",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # Zona Norte - Huechuraba
        {
            "nombre": "Lider Vivo Panorámico",
            "cadena": "Lider",
            "direccion": "Av. El Rodeo 12.955",
            "comuna": "Huechuraba",
            "ciudad": "Santiago",
            "latitud": -33.3650,
            "longitud": -70.6510,
            "telefono": "+56 2 2950 6000",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # Zona Ñuñoa
        {
            "nombre": "Unimarc Ñuñoa",
            "cadena": "Unimarc",
            "direccion": "Av. Irarrázaval 4090",
            "comuna": "Ñuñoa",
            "ciudad": "Santiago",
            "latitud": -33.4570,
            "longitud": -70.6010,
            "telefono": "+56 2 2680 9100",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Plaza Egaña",
            "cadena": "Santa Isabel",
            "direccion": "Av. Irarrázaval 5650",
            "comuna": "Ñuñoa",
            "ciudad": "Santiago",
            "latitud": -33.4620,
            "longitud": -70.5830,
            "telefono": "+56 2 2425 8100",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # Zona Peñalolén
        {
            "nombre": "Tottus Plaza Vespucio",
            "cadena": "Tottus",
            "direccion": "Av. Américo Vespucio 1501",
            "comuna": "Peñalolén",
            "ciudad": "Santiago",
            "latitud": -33.4890,
            "longitud": -70.5810,
            "telefono": "+56 2 2530 1000",
            "horario": "Lun-Dom 8:30-22:30"
        }
    ]
    
    # Insertar supermercados
    count_nuevos = 0
    for super_data in supermercados_ejemplo:
        # Verificar si ya existe
        existe = db.query(Supermercado).filter(
            Supermercado.nombre == super_data["nombre"]
        ).first()
        
        if not existe:
            supermercado = Supermercado(**super_data)
            db.add(supermercado)
            count_nuevos += 1
            print(f"[OK] Agregado: {super_data['nombre']} - {super_data['comuna']}")
        else:
            print(f"[--] Ya existe: {super_data['nombre']}")
    
    db.commit()
    print(f"\n{count_nuevos} supermercados nuevos agregados a la base de datos.")
    print(f"Total de supermercados en la BD: {db.query(Supermercado).count()}")
    db.close()


if __name__ == "__main__":
    print("=== Poblando base de datos con supermercados de Santiago, Chile ===\n")
    poblar_supermercados()
    print("\n¡Listo! La base de datos ha sido poblada.")
