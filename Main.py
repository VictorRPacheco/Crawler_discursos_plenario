from datetime import datetime
from selenium import webdriver

import time
import gspread
import re


class Bot:
    # Construtor
    def __init__(self):
        # Data do discurso a ser buscado
        data_inicio = "01/06/2021"
        data_fim = "30/06/2021"
        # Palavras a buscar
        palavras_chave = "covid+OR+pandemia+OR+coronavírus"

        # Página pra começar a ler
        self.pag_alvo_num = 1
        # Número da última página
        self.num_ultima_pag = 100


        self.pag_alvo_ini = "https://www.camara.leg.br/internet/sitaqweb/resultadoPesquisaDiscursos.asp?txIndexacao=&CurrentPage="
        self.pag_alvo_fim = "&BasePesq=plenario&txOrador=&txPartido=&dtInicio=" + data_inicio + "&dtFim=" + data_fim + "&txUF=&txSessao=&listaTipoSessao=&listaTipoInterv=&inFalaPres=&listaTipoFala=&listaFaseSessao=&txAparteante=&listaEtapa=&CampoOrdenacao=dtSessao&TipoOrdenacao=ASC&PageSize=50&txTexto=" + palavras_chave + "&txSumario="

        # TODO Atualizar para novo padrao de uso do geckdriver
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("intl.accept_languages", "pt,pt-BR")
        firefox_profile.set_preference("dom.webnotifications.enabled", False)
        try:
            self.driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path=r"geckodriver.exe")
        except Exception as e:
            print(f"{datetime.now()} STATUS BOT: Erro ao abrir o geckdriver. Erro: {e}")
        self.planilha = PlanilhaGoogle()
        print(f"Iniciando da página: {self.pag_alvo_num}")
        self.driver.get(self.pag_alvo_ini + str(self.pag_alvo_num) + self.pag_alvo_fim)
        time.sleep(2)

    def varrer_pagina(self):
        links = self.driver.find_elements_by_xpath("//span[@class='glyphicon glyphicon-file']")
        for i in range(len(links)):
            try:
                time.sleep(3)
                links = self.driver.find_elements_by_xpath("//span[@class='glyphicon glyphicon-file']")
                links[i].click()
                self.pegar_e_escrever_dados()
                self.driver.back()
            except:
                print(f"Erro na linha {i}")
                self.planilha.preenche_planilha("Erro")
                time.sleep(2)
                self.driver.get(self.pag_alvo_ini+str(self.pag_alvo_num)+self.pag_alvo_fim)
                time.sleep(3)
            time.sleep(2)

    def pegar_e_escrever_dados(self):
        time.sleep(3)
        dado_data = re.sub('Data: ', '', self.driver.find_element_by_xpath("//*[contains(text(), 'Data: ')]").text)
        dado_sessao = re.sub('Sessão: ', '', self.driver.find_element_by_xpath("//*[contains(text(), 'Sessão: ')]").text)
        dado_fase = re.sub('Fase: ', '', self.driver.find_element_by_xpath("//*[contains(text(), 'Fase: ')]").text)
        dado_orador = re.sub('Orador: ', '', self.driver.find_element_by_xpath("//*[contains(text(), 'Orador: ')]").text)
        dado_hora = re.sub('Hora: ', '', self.driver.find_element_by_xpath("//*[contains(text(), 'Hora: ')]").text)
        dado_link = self.driver.current_url
        dado_discurso = self.driver.find_element_by_xpath("//p[@align='justify']").text

        self.planilha.preenche_planilha(dado_data, dado_sessao, dado_fase, dado_orador, dado_hora, str(dado_link), dado_discurso)

    def proxima_pagina(self):
        if self.pag_alvo_num < self.num_ultima_pag:
            time.sleep(5)
            self.pag_alvo_num += 1
            self.driver.get(self.pag_alvo_ini+str(self.pag_alvo_num)+self.pag_alvo_fim)
            print(f"Indo pra página: {self.pag_alvo_num} -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            return 1
        else:
            return 0

class PlanilhaGoogle:
    # Construtor
    def __init__(self):
        # Acessa a conta de serviço
        self.gc = gspread.service_account("service_account.json")
        # atribui a primeira página da planilha
        self.planilha = self.gc.open("[Engie] Protocolos atendimento").sheet1
        # Busca a próxima linha vazia
        cols = self.planilha.range(1, 1, self.planilha.row_count, 2)
        self.linhaLivre = max([cell.row for cell in cols if cell.value]) + 1

    def preenche_planilha(self, data=0, sessao=0, fase=0, orador=0, hora=0, link=0, discurso=0):
        # print(f"{datetime.now()} STATUS GSpread: Preenchendo planilha")
        dados_anotar = [data, sessao, fase, orador, hora, link, discurso]
        print(dados_anotar)
        for i in range(len(dados_anotar)):
            self.planilha.update_cell(self.linhaLivre, i+1, str(dados_anotar[i]))
        self.linhaLivre += 1

bot = Bot()
time.sleep(10)
bot.varrer_pagina()
while bot.proxima_pagina():
    time.sleep(5)
    bot.varrer_pagina()
print("CONCLUIDOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")

