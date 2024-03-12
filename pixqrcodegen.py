import crcmod
import qrcode


class Payload():
    def __init__(self, nome, chavePix, valor, cidade, txtId):
        self.nome = nome
        self.chave_pix = chavePix
        self.valor = valor
        self.cidade = cidade
        self.txtId = txtId

        self.nome_tam = len(self.nome)
        self.chave_pix_tam = len(self.chave_pix)
        self.valor_tam = len(self.valor)
        self.cidade_tam = len(self.cidade)
        self.txtId_tam = len(self.txtId)


      
        self.merchantAccount_code = f'0014BR.GOV.BCB.PIX01{self.chave_pix_tam}{self.chave_pix}'

        if self.valor_tam <= 9:
            self.transactionAmount_code = f'0{self.valor_tam}{self.valor}'
        else:
            self.transactionAmount_code = f'{self.valor_tam}{self.valor}'

        if self.txtId_tam <= 9:
            self.addDataField_code = f'050{self.txtId_tam}{self.txtId}'
        else:
            self.addDataField_code = f'05{self.txtId_tam}{self.txtId}'
        
        if self.nome_tam <= 9:
            self.nome_tam = f'0{self.nome_tam}'

        if self.cidade_tam <= 9:
            self.cidade_tam = f'0{self.cidade_tam}'



        self.payloadFormat = '000201'
        self.merchantAccount = f'26{len(self.merchantAccount_code)}{self.merchantAccount_code}'
        self.transactionAmount = f'54{self.transactionAmount_code}'
        self.merchantCategCode = '52040000'
        self.transactionCurrency = '5303986'
        self.countryCode = '5802BR'
        self.merchantName = f'59{self.nome_tam}{self.nome}'
        self.merchantCity = f'60{self.cidade_tam}{self.cidade}'
        self.addDataField = f'62{len(self.addDataField_code)}{self.addDataField_code}'
        self.crc16 = '6304'

    def gerar_payload(self):
        self.payload = f'{self.payloadFormat}{self.merchantAccount}{self.merchantCategCode}{self.transactionCurrency}{self.transactionAmount}{self.countryCode}{self.merchantName}{self.merchantCity}{self.addDataField}{self.crc16}'

        self.gerar_crc16(self.payload)

        
    def gerar_crc16(self, payload):
        crc16 = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, 
        rev=False, xorOut=0x0000)
        
        self.crc16Code = hex(crc16(str(payload).encode('utf-8')))

        self.crc16Code_formatado = str(self.crc16Code).replace('0x', '').upper()

        self.payload_completa = f'{payload}{self.crc16Code_formatado}'

        print(f'\n{self.payload_completa}')
        self.gerarQRCode(self.payload_completa)

    def gerarQRCode(self, payload):
        self.qrcode = qrcode.make(payload)
        self.qrcode.save('pixqrcode.png')

if __name__ == '__main__':
    nome = input('Digite seu nome completo: ')
    chave_pix = input('Digite a chave PIX: ')
    valor = input('Digite o valor em reais: ')
    p = Payload(nome, chave_pix, valor,'cidade','DuzaoQRCode')
    p.gerar_payload()
