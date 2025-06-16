# app/db_init.py

from app.models.log_model import Base, engine

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")
