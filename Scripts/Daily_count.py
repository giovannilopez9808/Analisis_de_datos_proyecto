from Functions import *
import pandas as pd
import os


def create_daily_dataframe(index: list) -> DataFrame:
    """ 
    Crea un dataframe dado un indice y con una columna de titulo count
    """
    data = pd.DataFrame(index=index,
                        columns=["Count"])
    # Header del index, este aparecera al momento de guardar el documento
    data.index.names = ["Date"]
    # Inicializacion del conteo
    data = data.fillna(0)
    return data


parameters = {"path data": "../Data/",
              "path output": "../Output/",
              "useless columns": ["Usuario_Id",
                                  "Genero",
                                  "Año_de_nacimiento",
                                  "Inicio_del_viaje",
                                  "Fin_del_viaje",
                                  "Origen_Id",
                                  "Destino_Id"]}
# Obtiene el nombre de la base de datos de los archivos
files = obtain_filenames(parameters["path data"])
# Obtiene el periodo en la que se encuentran los datos
period = obtain_period_from_filenames(files)
# Obtiene los dias consecutivos entre el periodo obtenido
dates = obtain_consecutive_dates_from_period(period)
# Creacion del dataframe que guardara los conteos de cada estacion
daily_count = create_daily_dataframe(dates)
# Ciclo para variar entre los archivos
for file in files:
    print("Analizando archivo {}".format(file))
    # Lectura de los datos
    data = read_data(parameters["path data"],
                     file)
    # Convierte a formato de fecha el inicio del viaje
    data.index = pd.to_datetime(data["Inicio_del_viaje"])
    # Eliminacion de las columnas que no seran usadas
    data = data.drop(columns=parameters["useless columns"])
    # Calcula el conteo diario de los viajes
    data = data.resample("D").count()
    for index in data.index:
        # Obtiene la fecha del conteo
        date = (data["Viaje_Id"][index])
        # Guardado del conteo
        daily_count["Count"][index.date()] = date
# Impresion de los resultados
daily_count.to_csv("{}Daily_count.csv".format(parameters["path output"]))
