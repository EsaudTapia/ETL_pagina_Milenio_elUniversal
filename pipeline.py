import datetime
#Permite invocar comandos del sistema operativo
import subprocess
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

#Definimos una lista con los diferentes sites_uids
news_sites_uids = ['milenio']

#Función principal que ejecuta el ETL paso a paso
def main():
    _extract()
    _transform()
    _load()
    logger.info('..::Proceso ETL finalizado::..')

#Función encargada de invocar el proceso de extracción
def _extract():
    logger.info('..::Iniciando el proceso de extracción::..')

    #Iteramos en cada uno de los news_sites que tenemos en la lista
    for news_site_uid in news_sites_uids:
        #Corremos un subprocesopara ejecutar la primera etapa de extracción en la carpeta /extract
        #python main.py eluniversal
        subprocess.run(['python', 'main.py', news_site_uid], cwd='./extract')
        
        #Movemos los archivos csv generados al directorio transform
        subprocess.run(['move', r'extract\*.csv', r'transform'], shell=True)

#Función encargada de invocar el proceso de transformación
def _transform():
    logger.info('..::Iniciando el proceso de transformación::..')
    now = datetime.datetime.now().strftime('%Y_%m_%d')

    #Iteramos en cada uno de los news_sites que tenemos en la lista
    for news_site_uid in news_sites_uids:
        
        #Formando el nombre del archivo a procesar
        dirty_data_filename = '{}_{datetime}_articles.csv'.format(news_site_uid, datetime=now)
        #Corremos un subproceso para ejecutar la segunda etapa de extracción en la carpeta /transform
        subprocess.run(['python', 'main.py', dirty_data_filename], cwd='./transform')
        #Borramos todos los data set sucios
        subprocess.run(['del', dirty_data_filename], shell=True, cwd='./transform')
        #Movemos los archivos csv generados al directorio load
        subprocess.run(['move', r'transform\*.csv', r'load'], shell=True)

#Función encargada de invocar el proceso de carga
def _load():
    logger.info('..::Iniciando el proceso de carga::..')
    now = datetime.datetime.now().strftime('%Y_%m_%d')

    #Iteramos en cada uno de los news_sites que tenemos en la lista
    for news_site_uid in news_sites_uids:
        
        #Formando el nombre del archivo a procesar
        clean_data_filename = 'clean_{}_{datetime}_articles.csv'.format(news_site_uid, datetime=now)
        #Corremos un subproceso para ejecutar la tercera etapa de extracción en la carpeta /load
        subprocess.run(['python', 'main.py', clean_data_filename], cwd='./load')
        #Borramos todos los data set limpios
        subprocess.run(['del', clean_data_filename], shell=True, cwd='./load')

if __name__ == '__main__':
    main()