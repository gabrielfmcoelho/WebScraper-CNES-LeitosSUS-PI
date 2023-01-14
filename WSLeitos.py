from WebScraper import WS_CNES_Leitos

if __name__ == '__main__':
	
	print('')
	ano_inicio = int(input('Digite o ano de inicio [Permitido 2016 a 2022]: '))
	ano_fim = int(input('Digite o ano de termino [Permitido 2016 a 2022]: '))
	mes_inicio = int(input('Digite o mes de inicio [Permitido 1 a 12]: '))
	mes_fim = int(input('Digite o mes de termino [Permitido 1 a 12]: '))
	mun_esp_bool = input("O padrão é recolher os dados de todos os municipios do estado. Voce prefere escolher municipios especificos? [SIM ou NAO]: ")
	if mun_esp_bool.upper() == 'SIM':
		mun_esp_bool = True
		mun_esp_cod = str(input("Digite em formato de lista os codigos dos municipios do piaui que deseja analisar, exemplo -> ['220069','220425',...]: "))
		mun_esp_nome = str(input("Digite em formato de lista os nomes dos municipios do piaui que deseja analisar na mesma ordem de inserção da configuração passada, exemplo -> ['Teresina','Bom Jesus',...]: "))
	else:
		mun_esp_bool = False
		mun_esp_cod = []
		mun_esp_nome = []
	salvar_bool = input("Deseja salvar .csv independente de cada mes de cada municipio analisado [SIM, NAO]? ")
	if salvar_bool.upper() == 'SIM':
		salvar_bool = True
	else:
		salvar_bool = False
	
	WS_CNES_Leitos(ano_inicio, ano_fim, mes_inicio, mes_fim, mun_esp_bool, mun_esp_cod, mun_esp_nome, salvar_bool)
	