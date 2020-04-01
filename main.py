import xarray as xr
import pandas as pd
from bson.objectid import ObjectId
import src.agregadoBase
from src.agregadoBase import construtorDeCaminhos
from src.agregadoObs import observada
from src.dicionarioBase import merge_early as dicionario
from datetime import datetime, timedelta

#from src.mongo_src.mongo_needs import cmongo
#from src.mongo_src.mongo_needs import base_document_observado as bdo

    
path = r'/mnt/c/users/urca/downloads/smap-master/smap-master/base/dev/postos_plu'

def file_name(data):

    return 'MERGE_GPM_early_' + data.strftime("%Y%m%d%H.grib2")

def base():
    p = construtorDeCaminhos(path)
    
    aux = []
    dicionario = p.construct()
    for i in dicionario:

        for j in dicionario[i]:

            df = pd.read_csv(j, header=None, delim_whitespace=True, names=['cod', 'longitude', 'latitude'], dtype={'cod':object})
            df['bacia'] = i
            aux.append(df)
        
    base = pd.concat(aux)
    base.set_index(['latitude', 'longitude'], inplace=True)
    
    return base[~base.index.duplicated()]# .to_xarray()

def observado(fileName):

    # file = 'MERGE_GPM_early_'+ datetime.strftime(datetime(2020,2,27) + timedelta(hours=37), "%Y%m%d%H") + '.grib2'
    # file = 'MERGE_GPM_early_2020022923.grib2'
    file = fileName
    obs = observada(file)
    obs.dataSet_Chuva = obs.alteraValor()

    return obs.dataSet_Chuva

def retro_dictify(frame):
     d = {}
     for row in frame.values:
         here = d
         for elem in row[:-2]:
             if elem not in here:
                 here[elem] = {}
             here = here[elem]
         here[row[-2]] = row[-1]
     return d

def astypeString(frame):
    return frame.cod.astype(str)

def time_to_string(frame):
    return frame.time.apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))


if __name__=='__main__':

    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client["teste"]
    teste = db['teste']

    base = base()
    base_aray = base.to_xarray()

    obs = observado()
        
        #print(type(obs), type(base))

    interpolado = obs.interp(longitude=base_aray.longitude, latitude=base_aray.latitude)

    dataframe = interpolado.to_dataframe()
        #print(type(dataframe), '\n', dataframe.index)

    
    a['bacia'] = base.bacia
    a['cod'] = base.cod
    final = a[['bacia','cod', 'time', 'prec']]

    final.cod = astypeString(final)
        #final.time = time_to_string(final)

    dictfy = retro_dictify(final)

    final2 = final.reset_index()[['bacia', 'cod', 'prec']]

    dici = final2.groupby('bacia').apply(lambda x: dict(zip(x.cod, x.prec))).to_dict().copy()
    data = final.time.dt.to_pydatetime()[0].replace(hour=0)

    if teste.find_one({'data': data}) is None: 
        base_to_mongo = dicionario(final).create()
        teste.insert(base_to_mongo)

    for i in dici:
        for j in dici[i]:
            teste.update({ 'data':data}, { '$push':{ 'postos.' + str(i) + '.' + str(j): dici[i][j]  }  })
