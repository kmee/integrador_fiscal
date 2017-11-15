
from integrador_fiscal import BibliotecaIntegrador
from integrador_fiscal import ClienteIntegradorLocal
cliente = ClienteIntegradorLocal(BibliotecaIntegrador(
    '/opt/integrador/'),
    codigo_ativacao='12345678')

resposta = cliente.consultar_sat()
print resposta.mensagem