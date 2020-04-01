from datetime import datetime

class merge_early(object):

	def __init__(self, frame):

		self.data = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
		self.__frame = frame

	def create(self):
		print('aqui')
		#print(self.__frame)
		dicionario_auxiliar = base_documment_observado(self.__frame).dictify_frame()
		print('aqui2')
		dicionario_principal = {'data': self.data, 'doc': 'mrege_early', 'postos': dicionario_auxiliar}
		print("Classe Merge_early método create(), dicionario_principal:\n\n\n", dicionario_principal)
		print("\n"*100)

		return dicionario_principal

class base_documment_observado(object):

	def __init__(self, frame):

		self.__frame = frame.set_index('bacia')[['cod']]
		self.__dicionario = self.dictify_frame()

	@property
	def dicionario(self):
		return self.__dicionario
	
	def dictify_frame(self):
		print('aqui')
		frame = self.__frame

		frame['lista'] = ''
		dicionario = frame.groupby('bacia').apply(lambda x: dict(zip(x.cod, x.lista))).to_dict().copy()
		print("\n"*100)
		dicionario = iter_dictify(dicionario)
		print("\n"*100)

		return dicionario

def iter_dictify(dicionario):

	for key in dicionario:

		for key2 in dicionario[key]:

			dicionario[key][key2] = [] 

	return dicionario


