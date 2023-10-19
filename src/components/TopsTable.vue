<template>
  <div class="tops-table">
    <h2>Artilheiros</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Time</th>
            <th>Jogador</th>
            <th>Gols</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(player, index) in artilharia" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ player.Time }}</td>
            <td>{{ player.Nome }}</td>
            <td>{{ player.Gols }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import artilharia from '../../artilheiros.json';

export default {
  name: 'TopsTable',
  data() {
    return {
      artilharia: [],
    };
  },
  mounted() {
    // Carrega os dados da artilharia do arquivo JSON
    this.artilharia = artilharia.artilharia;
  },
};
</script>

<style scoped>
/* Estilos para centralizar a tabela na tela */
.tops-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* Isso centraliza verticalmente na tela */
}

/* Estilos para a tabela */
table {
  border-collapse: collapse;
  margin: 0px; /* Espaço ao redor da tabela */
  width: 150vh; /* Largura da tabela */
}

/* Estilos para a div que envolve a tabela */
.table-container {
  max-height: 80vh; /* Defina a altura máxima da tabela */
  overflow-y: auto; /* Adicione uma barra de rolagem vertical */
}

/* Estilos para as células da tabela */
th, td {
  border: 1px solid #ddd; /* Borda de 1 pixel com cor cinza */
  padding: 8px;
  text-align: left;
  background-color:  rgb(255, 255, 255, 0.5); /* Cor de fundo das linhas pares */
}

/* Estilos para as linhas ímpares da tabela */
tr:nth-child(odd) {
  background-color: #f2f2f2; /* Cor de fundo das linhas ímpares */
}

/* Estilos para cabeçalho da tabela */
th {
  background-color: #4CAF50; /* Cor de fundo para o cabeçalho */
  color: white; /* Cor do texto do cabeçalho */
}
</style>