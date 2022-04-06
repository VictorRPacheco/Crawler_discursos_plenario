# Crawler_discursos_plenario
Um crawler para coletar os dados e discursos do site https://www.camara.leg.br/ e colocar em uma planilha google.

Para rodar este código é necessário criar um arquivo de configuração da planilha google para onde será realizada a transcrição do dados coletados. Para isso crie um arquivo service_account.json e coloque junto a pasta raiz do código. Há um exemplo para auxiliar.

## Especificações do sistema
* Windows 11 - 64 bits
* Python 3.10
* Geckodriver 0.30.0 para windows 64 bits (https://github.com/mozilla/geckodriver/releases)