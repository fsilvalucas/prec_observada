import pandas as pd
import os
from datetime import datetime, timedelta

from src.dicionarioBase import merge_early
from main import base
from main import observado
from main import astypeString
from main import file_name
from src.mongo_needs import cmongo

import sys

if __name__ == '__main__':

	teste = cmongo('teste', 'teste').collection
	base = base()
	base_aray = base.to_xarray()
	
	for n in range(2):
		file = file_name(datetime(2020,3,26) + timedelta(hours=11+n))
		obs = observado(file)
		interpolado = obs.interp(longitude=base_aray.longitude, latitude=base_aray.latitude)
		dataframe = interpolado.to_dataframe()
		dataframe.to_csv('teste.txt', sep=' ', mode='a')
		sys.exit()
		
		print(base)
		
		a = dataframe[dataframe.index.isin(base.index)]
		a = pd.concat([a, base], axis=1)

		final = a[['bacia','cod', 'time', 'prec']]
		# final.assign(cod=astypeString(final))
		final2 = final.reset_index()[['bacia', 'cod', 'prec']].copy()

		# # # MODELAR O DATAFRAME EM UM DICIONARIO PARA O MONGODB # # # 

		hora = int(final.time.dt.hour.unique()[0])
		print(hora, type(hora))
		data = final.time.dt.to_pydatetime()[0].replace(hour=0)

		dici = final2.groupby('bacia').apply(lambda x: dict(zip(x.cod, x.prec))).to_dict().copy()

		if teste.find_one({'data': data}) is None: 
			base_to_mongo = merge_early(final).create()
			teste.insert(base_to_mongo)

		for i in dici:
			for j in dici[i]:
				teste.update({ 'data':data}, { '$push':{ 'postos.' + str(i) + '.' + str(j): dici[i][j]  }  })