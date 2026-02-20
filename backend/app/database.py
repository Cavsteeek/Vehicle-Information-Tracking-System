from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Render uses 'postgres://', but SQLAlchemy requires 'postgresql://'
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    

temp_engine = create_engine(DATABASE_URL)
with temp_engine.connect() as conn:
    # This creates the schema ONLY if it doesn't exist
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS vehicle_monitor"))
    conn.commit()
temp_engine.dispose()

engine = create_engine(DATABASE_URL, pool_pre_ping=True,
                       connect_args={"options": "-csearch_path=vehicle_monitor"}
                       )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
