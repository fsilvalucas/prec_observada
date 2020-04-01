import xarray as xr
# import pandas as import pd


class observadaForSmap(object): # Objeto de valor

    def __init__(self, xrDataset):

        self.__observada = xrDataset
    
    @property
    def observada(self):

        return self.__observada

    @observada.setter
    def observada(self, valor):

        self.__observada = valor
    
    def transforma_longitude(self):

        self.observada.coords['longitude'] = ((self.observada.coords['longitude'] + 180) % 360) - 180

        return self
    
    def slice_americaLatina(self):

        self.observada = self.observada.sel(longitude=slice(-82.2, -34.0), latitude=slice(-49.8, 12.2))
        
        return self
    


class observada(object): # Objeto de ENTIDADE

    def __init__(self, DocumentoDeChuvaObservada):

        self.__dataSet_Chuva = xr.open_dataset(DocumentoDeChuvaObservada, engine='cfgrib')
    
    @property
    def dataSet_chuva(self):
        
        return self.__dataSet_Chuva
    
    @dataSet_chuva.setter
    def dataSet_chuva(self, valor):

        self.__dataSet_Chuva = valor
    
    def alteraValor(self):

        return observadaForSmap(self.dataSet_chuva).transforma_longitude().slice_americaLatina().observada

 #def leitura_chuva_observada(file):   
    
#    ds = xr.open_dataset(file, engine='cfgrib') # Lê o documento de chuva

#    ds.coords['longitude'] = ((ds.coords['longitude'] + 180) % 360) - 180 # Altera a longitude de 0 a 360 para -180 a 180

 #   ds = ds.sel(longitude=slice(-82.2, -34.0), latitude=slice(49.8, 12.2)) # Slice para apenas á America Latina

  #  return ds



