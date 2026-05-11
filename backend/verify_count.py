from app.database import SessionLocal
from app.models import Supermercado
from sqlalchemy import func

db = SessionLocal()

count = db.query(Supermercado).count()
print(f'\n=== VERIFICACION FINAL ===')
print(f'Total de supermercados en BD: {count}')

# Top 10 comunas
comunas = db.query(Supermercado.comuna, func.count(Supermercado.id)).group_by(Supermercado.comuna).order_by(func.count(Supermercado.id).desc()).limit(10).all()
print(f'\nTop 10 comunas con más supermercados:')
for comuna, c in comunas:
    comuna_name = comuna if comuna else "Sin comuna"
    print(f'  {comuna_name:30} {c:4} supermercados')

db.close()
