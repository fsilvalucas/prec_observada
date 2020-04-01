from src.agregadoObs import observada

file = 'MERGE_GPM_early_2020021810.grib2'
obs = observada(file)
obs.dataSet_Chuva = obs.alteraValor()

print(obs.dataSet_Chuva.to_dataframe())