# Importe as funções dos módulos correspondentes
from import_jogos_BD import atualizar_jogos
from import_news_BD import atualizar_noticias
from import_table_BD import atualizar_tabela
from import_tops_BD import atualizar_tops
from cria_usuarioBD import cria_User

#Cria tabela de usuario no bd se n exixtir
cria_User()

# Atualize o banco de dados
atualizar_noticias()
print("Atualizações 1/4")
atualizar_tops()
print("Atualizações 2/4")
atualizar_tabela()
print("Atualizações 3/4")
atualizar_jogos()
print("Atualizações 4/4")
print("Atualizações concluídas com sucesso!")
