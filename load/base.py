from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Declaramos el motor de BD a usar
engine = create_engine('sqlite:///newspaper.db')

#Creamos una nueva session
Session = sessionmaker(bind=engine)

#Creamos el objeto de la base de datos
Base = declarative_base()