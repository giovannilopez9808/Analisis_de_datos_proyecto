from Functions import *

parameters = {"path output": "../Output/",
              "path data": "../Data/",
              "path information": "../Information/",
              "file distances": "Distance_between.csv",
              "file output": "Daily_distance.csv",
              "useless columns": ["Usuario_Id",
                                  "Genero",
                                  "Viaje_Id",
                                  "Año_de_nacimiento"]
              }

files = obtain_filenames(parameters["path data"])
period = obtain_period_from_filenames(files)
dates = obtain_consecutive_dates_from_period(period)
daily_data_output = create_daily_dataframe(dates,
                                           header=["Mean", "Var"],
                                           use_float=True)
distance_data = read_data(parameters["path output"],
                          parameters["file distances"],
                          use_index=True)
for file in files:
    print("Analizando archivo {}".format(file))
    data = read_data(parameters["path data"],
                     file)
    distances = distance_algorithm(data,
                                   parameters["useless columns"],
                                   distance_data,
                                   distance_data.index)
    data = distances.data
    daily_mean_data = data.resample("D").mean()
    daily_var_data = data.resample("D").var()
    del data
    for date in daily_mean_data.index:
        index = date.date()
        value = daily_mean_data["Distance"][date]
        daily_data_output.loc[index, "Mean"] = value
        value = daily_var_data["Distance"][date]
        daily_data_output.loc[index, "Var"] = value
    del daily_mean_data, daily_var_data
daily_data_output.to_csv("{}{}".format(parameters["path output"],
                                       parameters["file output"]))
