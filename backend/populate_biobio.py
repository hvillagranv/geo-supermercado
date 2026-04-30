"""
Script para agregar supermercados de la Región del Biobío
Comunas: Talcahuano, Concepción, San Pedro de la Paz, Coronel, Lota, Chiguayante, Penco y Tomé
"""
from app.database import SessionLocal
from app.models import Supermercado
from datetime import datetime

def poblar_supermercados_biobio():
    db = SessionLocal()
    
    # Supermercados de la Región del Biobío
    supermercados_biobio = [
        # CONCEPCIÓN
        {
            "nombre": "Jumbo Concepción Centro",
            "cadena": "Jumbo",
            "direccion": "Av. O'Higgins 940",
            "comuna": "Concepción",
            "ciudad": "Concepción",
            "latitud": -36.8270,
            "longitud": -73.0498,
            "telefono": "+56 41 2740 000",
            "horario": "Lun-Dom 8:00-23:00"
        },
        {
            "nombre": "Lider Concepción",
            "cadena": "Lider",
            "direccion": "Av. Los Carrera 555",
            "comuna": "Concepción",
            "ciudad": "Concepción",
            "latitud": -36.8201,
            "longitud": -73.0444,
            "telefono": "+56 41 2950 100",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Unimarc Freire",
            "cadena": "Unimarc",
            "direccion": "Av. Ramón Freire 550",
            "comuna": "Concepción",
            "ciudad": "Concepción",
            "latitud": -36.8310,
            "longitud": -73.0520,
            "telefono": "+56 41 2680 200",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Barros Arana",
            "cadena": "Santa Isabel",
            "direccion": "Barros Arana 871",
            "comuna": "Concepción",
            "ciudad": "Concepción",
            "latitud": -36.8265,
            "longitud": -73.0510,
            "telefono": "+56 41 2425 100",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Tottus Mall del Centro",
            "cadena": "Tottus",
            "direccion": "Av. Arturo Prat 599",
            "comuna": "Concepción",
            "ciudad": "Concepción",
            "latitud": -36.8255,
            "longitud": -73.0475,
            "telefono": "+56 41 2530 200",
            "horario": "Lun-Dom 8:30-22:30"
        },
        
        # TALCAHUANO
        {
            "nombre": "Jumbo Talcahuano",
            "cadena": "Jumbo",
            "direccion": "Av. Colón 3900, Mall Plaza El Trébol",
            "comuna": "Talcahuano",
            "ciudad": "Talcahuano",
            "latitud": -36.7130,
            "longitud": -73.1140,
            "telefono": "+56 41 2959 300",
            "horario": "Lun-Dom 8:00-23:00"
        },
        {
            "nombre": "Lider El Trébol",
            "cadena": "Lider",
            "direccion": "Av. Jorge Alessandri 3177",
            "comuna": "Talcahuano",
            "ciudad": "Talcahuano",
            "latitud": -36.7145,
            "longitud": -73.1155,
            "telefono": "+56 41 2950 400",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Unimarc Talcahuano Centro",
            "cadena": "Unimarc",
            "direccion": "Av. Colón 145",
            "comuna": "Talcahuano",
            "ciudad": "Talcahuano",
            "latitud": -36.7220,
            "longitud": -73.1170,
            "telefono": "+56 41 2680 300",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Talcahuano",
            "cadena": "Santa Isabel",
            "direccion": "Av. San Martín 1250",
            "comuna": "Talcahuano",
            "ciudad": "Talcahuano",
            "latitud": -36.7280,
            "longitud": -73.1190,
            "telefono": "+56 41 2425 200",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # SAN PEDRO DE LA PAZ
        {
            "nombre": "Jumbo San Pedro",
            "cadena": "Jumbo",
            "direccion": "Av. Michimalonco 1401, Mall Plaza Los Ángeles",
            "comuna": "San Pedro de la Paz",
            "ciudad": "San Pedro de la Paz",
            "latitud": -36.8485,
            "longitud": -73.0965,
            "telefono": "+56 41 2959 500",
            "horario": "Lun-Dom 8:00-23:00"
        },
        {
            "nombre": "Lider San Pedro",
            "cadena": "Lider",
            "direccion": "Av. Padre Hurtado 2845",
            "comuna": "San Pedro de la Paz",
            "ciudad": "San Pedro de la Paz",
            "latitud": -36.8520,
            "longitud": -73.0990,
            "telefono": "+56 41 2950 600",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Tottus San Pedro",
            "cadena": "Tottus",
            "direccion": "Av. Padre Hurtado 3151",
            "comuna": "San Pedro de la Paz",
            "ciudad": "San Pedro de la Paz",
            "latitud": -36.8550,
            "longitud": -73.1010,
            "telefono": "+56 41 2530 300",
            "horario": "Lun-Dom 8:30-22:30"
        },
        {
            "nombre": "Unimarc Boca Sur",
            "cadena": "Unimarc",
            "direccion": "Av. Pedro de Valdivia 1500",
            "comuna": "San Pedro de la Paz",
            "ciudad": "San Pedro de la Paz",
            "latitud": -36.8395,
            "longitud": -73.0850,
            "telefono": "+56 41 2680 400",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # CHIGUAYANTE
        {
            "nombre": "Lider Chiguayante",
            "cadena": "Lider",
            "direccion": "Av. O'Higgins 2850",
            "comuna": "Chiguayante",
            "ciudad": "Chiguayante",
            "latitud": -36.9225,
            "longitud": -73.0295,
            "telefono": "+56 41 2950 700",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Unimarc Chiguayante",
            "cadena": "Unimarc",
            "direccion": "Av. Independencia 1780",
            "comuna": "Chiguayante",
            "ciudad": "Chiguayante",
            "latitud": -36.9250,
            "longitud": -73.0320,
            "telefono": "+56 41 2680 500",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Chiguayante",
            "cadena": "Santa Isabel",
            "direccion": "Av. Leonera 1456",
            "comuna": "Chiguayante",
            "ciudad": "Chiguayante",
            "latitud": -36.9210,
            "longitud": -73.0280,
            "telefono": "+56 41 2425 300",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # CORONEL
        {
            "nombre": "Lider Coronel",
            "cadena": "Lider",
            "direccion": "Av. Manuel Montt 1345",
            "comuna": "Coronel",
            "ciudad": "Coronel",
            "latitud": -37.0285,
            "longitud": -73.1510,
            "telefono": "+56 41 2950 800",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Unimarc Coronel",
            "cadena": "Unimarc",
            "direccion": "Av. Camilo Henríquez 950",
            "comuna": "Coronel",
            "ciudad": "Coronel",
            "latitud": -37.0310,
            "longitud": -73.1540,
            "telefono": "+56 41 2680 600",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Coronel",
            "cadena": "Santa Isabel",
            "direccion": "Av. Pedro Aguirre Cerda 1240",
            "comuna": "Coronel",
            "ciudad": "Coronel",
            "latitud": -37.0265,
            "longitud": -73.1495,
            "telefono": "+56 41 2425 400",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # LOTA
        {
            "nombre": "Unimarc Lota",
            "cadena": "Unimarc",
            "direccion": "Av. Carlos Cousiño 890",
            "comuna": "Lota",
            "ciudad": "Lota",
            "latitud": -37.0895,
            "longitud": -73.1565,
            "telefono": "+56 41 2680 700",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Lota",
            "cadena": "Santa Isabel",
            "direccion": "Av. Baldomero Lillo 1450",
            "comuna": "Lota",
            "ciudad": "Lota",
            "latitud": -37.0920,
            "longitud": -73.1585,
            "telefono": "+56 41 2425 500",
            "horario": "Lun-Dom 9:00-21:30"
        },
        
        # PENCO
        {
            "nombre": "Unimarc Penco",
            "cadena": "Unimarc",
            "direccion": "Av. Sotomayor 1250",
            "comuna": "Penco",
            "ciudad": "Penco",
            "latitud": -36.7385,
            "longitud": -72.9965,
            "telefono": "+56 41 2680 800",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Penco",
            "cadena": "Santa Isabel",
            "direccion": "Av. Manuel Bulnes 780",
            "comuna": "Penco",
            "ciudad": "Penco",
            "latitud": -36.7410,
            "longitud": -72.9985,
            "telefono": "+56 41 2425 600",
            "horario": "Lun-Dom 9:00-22:00"
        },
        
        # TOMÉ
        {
            "nombre": "Unimarc Tomé",
            "cadena": "Unimarc",
            "direccion": "Av. Latorre 1145",
            "comuna": "Tomé",
            "ciudad": "Tomé",
            "latitud": -36.6165,
            "longitud": -72.9575,
            "telefono": "+56 41 2680 900",
            "horario": "Lun-Dom 9:00-22:00"
        },
        {
            "nombre": "Santa Isabel Tomé",
            "cadena": "Santa Isabel",
            "direccion": "Av. Diego Portales 890",
            "comuna": "Tomé",
            "ciudad": "Tomé",
            "latitud": -36.6185,
            "longitud": -72.9595,
            "telefono": "+56 41 2425 700",
            "horario": "Lun-Dom 9:00-21:30"
        },
        {
            "nombre": "Lider Tomé",
            "cadena": "Lider",
            "direccion": "Av. Arturo Prat 1456",
            "comuna": "Tomé",
            "ciudad": "Tomé",
            "latitud": -36.6145,
            "longitud": -72.9555,
            "telefono": "+56 41 2950 900",
            "horario": "Lun-Dom 9:00-22:00"
        }
    ]
    
    # Insertar supermercados
    count_nuevos = 0
    count_existentes = 0
    
    print("=== Agregando supermercados de la Región del Biobío ===\n")
    
    for super_data in supermercados_biobio:
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
            count_existentes += 1
            print(f"[--] Ya existe: {super_data['nombre']}")
    
    db.commit()
    
    print(f"\n{'='*70}")
    print(f"RESUMEN:")
    print(f"  - Supermercados nuevos agregados: {count_nuevos}")
    print(f"  - Supermercados que ya existían: {count_existentes}")
    print(f"  - Total en la BD: {db.query(Supermercado).count()}")
    print(f"{'='*70}")
    
    # Mostrar distribución por comuna
    print(f"\nDistribución por comuna en Región del Biobío:")
    comunas_biobio = ["Concepción", "Talcahuano", "San Pedro de la Paz", "Chiguayante", 
                      "Coronel", "Lota", "Penco", "Tomé"]
    
    for comuna in comunas_biobio:
        count = db.query(Supermercado).filter(Supermercado.comuna == comuna).count()
        if count > 0:
            print(f"  - {comuna}: {count} supermercados")
    
    db.close()


if __name__ == "__main__":
    poblar_supermercados_biobio()
    print("\n[OK] Proceso completado!")
