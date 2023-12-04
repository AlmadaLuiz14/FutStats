# Importe as funções dos módulos correspondentes
from imports.import_jogos_Json import atualizar_jogos_Json
from imports.import_news_Json import atualizar_noticias_Json
from imports.import_table_Json import atualizar_tabela_Json
from imports.import_tops_Json import atualizar_tops_Json
from imports.import_assist_Json import atualizar_assist_Json
from imports.converte_TIME_assist import converte_time

#converte Json para BD
from imports.converte_artilheiros_JsonBD import converte_artilheiros
from imports.converte_tabela_JsonBD import converte_tabela
from imports.converte_jogos_JsonBD import converte_jogos
from imports.converte_noticias_JsonBD import converte_noticias
from imports.converte_assist_JsonBD import converte_assist
from imports.cria_usuarioBD import cria_User
from simulação.converte_simula import converte_simula

cria_User()
# Atualize os arquivos Json

atualizar_noticias_Json()
converte_noticias()
print("1/5")
atualizar_tops_Json()
converte_artilheiros()
print("2/5")
atualizar_tabela_Json()
converte_tabela()
converte_simula()
print("3/5")
atualizar_jogos_Json()
converte_jogos()
print("4/5")
atualizar_assist_Json()
converte_time()
converte_assist()
print("5/5")
print("Atualizações concluídas com sucesso!")
