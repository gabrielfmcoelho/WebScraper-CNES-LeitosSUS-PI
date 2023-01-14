print('')
print('VERIFICAÇÃO DE DEPENDENCIAS')
print('<><><><><><><><><><><><><><><><><><><>')
print('')

import os
try:
    os.system('pip install -r requirements.txt')
    os.system('pip install beautifulsoup4')
    os.system('pip install requests')
    print('')
except:
    print('')
	
print('<><><><><><><><><><><><><><><><><><><>')


# Importando bibliotecas
import pandas as pd
import requests
import urllib.request
import bs4
from bs4 import BeautifulSoup
import time
from IPython.display import clear_output


class WS_CNES_Leitos:
    
    def __init__(self, ano_inicial=2016, ano_final=2022, mes_inicial=1 , mes_final=12, bool_municip=False, municip_cod=[], municip_nome=[], salvar_mun=False):
        self.ano_inicial = ano_inicial
        self.ano_final = ano_final
        self.mes_inicial = mes_inicial
        self.mes_final = mes_final
        self.bool_municip = bool_municip
        self.municip_cod = municip_cod
        self.municip_nome = municip_nome
        self.salvar_mun = salvar_mun
        
        def converter_comp_p_data(i):
            data = str(i)
            dia_ficcional = '20'
            ano_data = data[:4]
            mes_data = data[4:]
            data_completa = dia_ficcional + '/' + mes_data + '/' + ano_data 
            return data_completa

        def converter_comp_p_ano(i):
            data = str(i)
            ano_data = data[:4]
            return int(ano_data)

        def converter_comp_p_mes(i):
            data = str(i)
            mes_data = data[4:]
            return int(mes_data)
        
        colunas_população = []
        competencias = []
        primeira_competencia = True
        contador_auxiliar = 1
        index_mun = 0

        dicionario_categorias = {'CIRÚRGICO':'Cirurgico',
                                'CLÍNICO':'Clinico',
                                'OBSTÉTRICO':'Obstetrico',
                                'PEDIATRICO':'Pediatrico',
                                'OUTRAS ESPECIALIDADES':'Outras Especialidades',
                                'HOSPITAL DIA':'Hospital Dia',
                                'COMPLEMENTAR':'Complementar'}

        for ano_pop in range(self.ano_inicial, (self.ano_final+1)):
            colunas_população.append(f'População {ano_pop}')

        nome_colunas_df = ['Competência', 'Ano', 'Mes', 'Código', 'Categoria', 'Descrição', 'Existente', 'SUS', '%Ocupação', 'Geocodigo', 'População']
        nome_colunas_df_completo = nome_colunas_df + ['País', 'Estado', 'Município', 'Mesoregião', 'Regional de Saúde']

        path_armazenamento_raiz = './Leitos_CNES_PI'
        path_armazenamento_mun = path_armazenamento_raiz + '/Municipios'
        path_auxiliar = './temp_WSS_CNES'
        path_csv_munpi = 'MunicipiosPI.csv'

        print('')
        print('INICIANDO PROCEDIMENTO DE WEB SCRAPING')
        print('Codigo preparado por Gabriel Coelho')
        print('Me encontre em: https://www.linkedin.com/in/gabriel--coelho/')
        print('<><><><><><><><><><><><><><><><><><><>')

        print('')
        print('...Criando diretorios')

        try:
            os.makedirs(path_auxiliar)
            print('> Diretorio temporario criado')
        except:
            print('> Diretorio temporario ja existente')

        try:
            os.makedirs(path_armazenamento_mun)
            print('> Diretorio de armazenamento criado')
        except:
            print('> Diretorio de armazenamento ja existente')

        print('')
        print('...Lendo dados')

        try:
            df_municipios = pd.read_csv(path_csv_munpi)
            print('> Banco de dados dos municipios do Piaui 2016 a 2022 - OK')
        except:
            print('> Banco de dados dos municipios do Piaui 2016 a 2022 - FALHOU')

        try:
            df_Leitos_CNES_PI_Completo = pd.read_csv(f'{path_armazenamento_raiz}/Leitos_CNES_PI_Completo.csv')
            print('> Banco de dados dos leitos CNES PI - OK')
        except:
            df_Leitos_CNES_PI_Completo = pd.DataFrame(columns=nome_colunas_df)
            df_Leitos_CNES_PI_Completo.to_csv(f'{path_armazenamento_raiz}/Leitos_CNES_PI_Completo.csv')
            print('> Banco de dados dos leitos CNES PI - Não existente -> Foi Criado')

        try:
            df_pular_mun_lista = pd.read_csv(f'{path_auxiliar}/pular_mun_lista.csv')
            print('> Planilhar auxiliar detectada...lendo')
        except:
            df_pular_mun_lista = pd.DataFrame(columns=['Geocodigo'])
            df_pular_mun_lista.to_csv(f'{path_auxiliar}/pular_mun_lista.csv')
            print('> Criando planilha auxiliar')

        print('')
        print('...Criando dados auxiliares')

        if self.bool_municip:
            municipios = self.municip_cod
            nome_município = self.municip_nome
        else:
            municipios = list(df_municipios['Geocodigo'])
            nome_município = list(df_municipios['Município'])
        dicionario_municipios = dict(zip(municipios, nome_município))

        try:
            for mun in municipios:
                for i in range(self.ano_inicial, (self.ano_final+1)):
                    for j in range(self.mes_inicial, (self.mes_final+1)):
                        if len(str(j)) < 2:
                            mes = f'0{j}'
                        else:
                            mes = j
                        ano = f'{i}{mes}'
                        if primeira_competencia:
                            competencias.append(ano)
                        for key, value in dicionario_municipios.items():
                            if (mun == key):
                                nome_mun = value
                                nome_mun = nome_mun.replace(' ','_')
                        nome_dataframe = f'df_Leitos_CNES_PI_{nome_mun}_{ano}'
                        vars()[nome_dataframe] = pd.DataFrame(columns=nome_colunas_df)
                primeira_competencia=False
            print('> Competencias e planilhas auxiliares - OK')
            print(f'> Inicio das competencias: {min(competencias)}, final das competencias: {max(competencias)}')
        except:
            print(print('> Competencias e planilhas auxiliares - FALHOU'))

        print('')
        print('...Analisando dados dos municipios')

        for mun in municipios:
            #try:
                pular_mun=False

                for key, value in dicionario_municipios.items():
                    if (mun == key):
                        nome_mun = value
                        nome_mun = nome_mun.replace(' ','_')


                if(pular_mun):
                    continue

                print('')
                print(f'...Iniciando {mun} - {nome_mun}: {index_mun+1}/224')
                print('---------------------------------')
                contador_auxiliar = contador_auxiliar + 1

                for i in competencias:
                    #try:

                        index_atual=0
                        ultimo_titulo=''
                        pular_proxima_linha=False
                        primeiro=True
                        controlador=True

                        informações = ['','','','','','','','','','','']

                        for index, row in df_pular_mun_lista.iterrows(): 
                            if(row['Geocodigo'] == mun):
                                #print(f'>> Pulando {nome_mun} - {i}')
                                pular_mun = True
                                index_atual = index_atual+1
                                break

                        if(pular_mun):
                            continue

                        print('')
                        print(f'...Iniciando {nome_mun} - {i}:')

                        try:
                            print('> Carregando pagina')
                            url = f'http://cnes2.datasus.gov.br/Mod_Ind_Tipo_Leito.asp?VEstado=22&VMun={mun}&VComp={i}'
                            pagina = urllib.request.urlopen(url)
                            soup = BeautifulSoup(pagina, 'html.parser')
                            tabela_bruta = soup.find_all('table')
                            tabela_filtrada = tabela_bruta[0].find('table', border=1, width=500, cellpadding=1, align='center')
                            print('>> Pagina carregada')
                        except:
                            print('!!!!Problema ao explorar html!!!!  Tentando novamente..' )
                            url = f'http://cnes2.datasus.gov.br/Mod_Ind_Tipo_Leito.asp?VEstado=22&VMun={mun}&VComp={i}'
                            pagina = urllib.request.urlopen(url)
                            soup = BeautifulSoup(pagina, 'html.parser')
                            tabela_bruta = soup.find_all('table')
                            tabela_filtrada = tabela_bruta[0].find('table', border=1, width=500, cellpadding=1, align='center')
                            print('>> Pagina carregada')

                        print('> Explorando a pagina')
                        if (type(tabela_filtrada) == bs4.element.Tag):
                            for linha in tabela_filtrada.find_all('tr'):

                                if (not primeiro):
                                    primeiro=True
                                    continue

                                if (pular_proxima_linha):
                                    pular_proxima_linha = (not pular_proxima_linha)
                                    continue

                                titulo_raw = linha.find('td', colspan=3)

                                if((type(titulo_raw) == bs4.element.Tag) and titulo_raw.text.strip() != ultimo_titulo):
                                    titulo = titulo_raw.text.strip()
                                    if(titulo != ultimo_titulo):
                                        ultimo_titulo = titulo
                                        pular_proxima_linha=True
                                        if(controlador):
                                            controlador = False
                                        else:
                                            primeiro = False
                                        continue

                                dados = linha.find_all('td')

                                if len(dados) > 4:
                                    break

                                print('>> Carregando informações')
                                informações[0] = converter_comp_p_data(i)
                                informações[1] = converter_comp_p_ano(i)
                                informações[2] = converter_comp_p_mes(i)
                                informações[3] = int(dados[0].text.strip())
                                informações[4] = ultimo_titulo
                                informações[5] = dados[1].text.strip()
                                informações[6] = int(dados[2].text.strip())
                                informações[7] = int(dados[3].text.strip())
                                informações[8] = round(float((informações[7])/float(informações[6])), 2)
                                informações[9] = mun
                                informações[10] = '0'

                                df_informações = pd.DataFrame([informações], columns=nome_colunas_df)
                                vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'] = pd.concat([vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'], df_informações], ignore_index=True)
                                index_atual = index_atual+1

                            vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}']['Competência'] = pd.to_datetime(vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}']['Competência'], format='%d/%m/%Y')

                            vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}']['Categoria'] = vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}']['Categoria'].map(dicionario_categorias)


                            print('>>> Merge com dados do municipio')
                            vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'] = pd.merge(vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'], df_municipios, on="Geocodigo", how="left", suffixes=('_x', '_y'))

                            print('>>> Identificando total populacional do periodo')
                            for index, row in vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'].iterrows():
                                for pop_ano in range(self.ano_inicial, (self.ano_final+1)):
                                    if (row['Ano'] == pop_ano):
                                        for index_mun_i, row_mun_i in df_municipios.iterrows():
                                            if(row['Geocodigo'] == row_mun_i['Geocodigo']):
                                                vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'].iloc[index,10] = df_municipios[f'População {pop_ano}'][index_mun_i]
                                                break
                                    else:
                                        continue
                                    break

                            vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'].drop(colunas_população, axis=1, inplace=True)

                            #vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'].reset_index(inplace=True, drop=True)
                            #df_Leitos_CNES_PI_Completo.reset_index(inplace=True, drop=True)

                            print('>>> Adicionando à planilha completa')
                            df_Leitos_CNES_PI_Completo = pd.concat([df_Leitos_CNES_PI_Completo, vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}']], ignore_index=True)

                            if self.salvar_mun:
                                print('>>> Salvando planilha especifica')

                                vars()[f'df_Leitos_CNES_PI_{nome_mun}_{i}'].to_csv(f'./Leitos_CNES_PI/Municipios/Leitos_CNES_PI_{nome_mun}_{i}.csv')

                            print(f'Dataset: {nome_mun} - {converter_comp_p_mes(i)}/{converter_comp_p_ano(i)} - OK')
                            #clear_output(wait=True)

                        else:
                            print('>> Exploração abortada')
                            print(f'Dataset: {nome_mun} - {converter_comp_p_mes(i)}/{converter_comp_p_ano(i)} - VAZIO')
                            #clear_output(wait=True)


                print('---------------------------------')
                print('>> Salvando dados')
                df_mun = pd.DataFrame([mun], columns=['Geocodigo'])
                df_pular_mun_lista = pd.concat([df_pular_mun_lista, df_mun], ignore_index=True)
                df_pular_mun_lista = df_pular_mun_lista.loc[:,df_pular_mun_lista.columns.isin(['Geocodigo'])]
                df_pular_mun_lista.to_csv(f'{path_auxiliar}/pular_mun_lista.csv', index=False)
                df_Leitos_CNES_PI_Completo = df_Leitos_CNES_PI_Completo.loc[:,df_Leitos_CNES_PI_Completo.columns.isin(nome_colunas_df_completo)]
                df_Leitos_CNES_PI_Completo.sort_values(['Ano', 'Mes', 'Código', 'Geocodigo'],ascending = [True, True, True, True])
                df_Leitos_CNES_PI_Completo.to_csv(f'{path_armazenamento_raiz}/Leitos_CNES_PI_Completo.csv', index=False)
                index_mun = index_mun + 1
                print('>>> Dados salvos')
                print('')
                print('...Limpando terminal')
                clear_output(wait=True)

                    #except(e):
                        #print(e)
                        #print(f'Dataset: {nome_mun} - {converter_comp_p_mes(i)}/{converter_comp_p_ano(i)} - FALHOU')

            #except(e):
                #print(e)
                #print(f'Municipio: {nome_mun} - FALHOU')

        print('... Finalizando')   
        df_Leitos_CNES_PI_Completo.to_csv('./Leitos_CNES_PI/Leitos_CNES_PI_Completo.csv', index=False)

        print('<><><><><><><><><><><><><><><><><><><>')

        print('')
        print('!!! Finalizado !!!')

        print('')
        print('...Vamos ver como é a forma do nosso banco de dados!')
        print('')
        print(df_Leitos_CNES_PI_Completo)

        print('')
        print('...Aqui está a descrição do banco de dados criado! Aproveite!')
        print('')
        df_Leitos_CNES_PI_Completo.info()