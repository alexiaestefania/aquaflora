#utilizando requests de python, conseguir resultados em xml, parse them and get their damn dtaa, passar dados dinamicamente
#cep destino - passar CEP do endereco padrao do usuario requisitando 
#uma vez parseado, mostrar o preco do frete e prazo na pagina

import requests
import xml.etree.ElementTree as ET

# http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?op=CalcPrecoPrazo
SEDEX = "40014"
PAC = "04510"
cep_origem = "01001000"
cep_destino = "12460000"
api_url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx/CalcPrecoPrazo"
payload = {
    "nCdEmpresa": "",
    "sDsSenha": "",
    "nCdServico": "40010",
    "sCepOrigem": "01001000",
    "sCepDestino": "12460000",
    "nVlPeso": "1",
    "nCdFormato": "1",  # 1 = caixa/pacote
    "nVlComprimento": "20",
    "nVlAltura": "2",
    "nVlLargura": "20",
    "nvlDiametro": "15",
    "sCdMaoPropria": "N",
    "nVlValorDeclarado": "0",
    "sCdAvisoRecebimento": "N",
    "StrRetorno": "xml",
}

# https://docs.python-requests.org/en/latest/user/quickstart/#make-a-request
r = requests.post(api_url, data=payload)

# https://docs.python.org/3.8/library/xml.etree.elementtree.html
root = ET.fromstring(r.text)
from pprint import pprint

pprint(r.text)
elements = root.findall("./{http://tempuri.org}Servicos")

pprint(elements)
