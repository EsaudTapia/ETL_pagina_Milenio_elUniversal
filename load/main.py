import argparse
import logging
import pandas as pd
from article import Article
from base import Base, engine, Session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def main(filename):
    #Generamos el esquema de la BD
    Base.metadata.create_all(engine)
    #Iniciamos sesión
    session = Session()
    #Leemos el archivo csv limpio
    articles = pd.read_csv(filename, encoding='utf-8')

    #Iteramos entre la filas del csv mediante el método iterrows() y vamos pasando los articulos a la BD
    for index, row in articles.iterrows():
        logger.info('Cargando el artículo con uid {} en la BD'.format(row['uid']))
        article = Article(row['uid'], 
                            row['body'], 
                            row['host'], 
                            row['title'], 
                            row['newspaper_uid'], 
                            row['n_tokens_body'], 
                            row['n_tokens_title'], 
                            row['url'])
        session.add(article)
        session.commit()
        session.close()

if __name__ == '__main__':
    #Creamos un nuevo parser de argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name',
                        help='La ruta al dataset limpio para cargar a la BD',
                        type=str)
    #Parseamos los argumentos.
    args = parser.parse_args()

    main(args.file_name)