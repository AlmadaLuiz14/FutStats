<template>
  <div class="tops-table">
    <h2>Artilheiros</h2>
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Jogador</th>
          <th>Posição</th>
          <th>Gols</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(player, index) in topScorers" :key="index">
          <td>{{ index+1 }}</td>
          <td>{{ player.name }}</td>
          <td>{{ player.position }}</td>
          <td>{{ player.goals }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'TopsTable',
  props: {
    msg: String
  },
  data() {
    return {
      topScorers: [
        { name: 'Neymar', position: 'Atacante', goals: 13 },
        { name: 'Gabigol', position: 'Atacante', goals: 11 },
        { name: 'Bruno Henrique', position: 'Atacante', goals: 7 },
        { name: 'Everton', position: 'Atacante', goals: 7 },
        { name: 'Pedro', position: 'Atacante', goals: 6 },
        { name: 'Lucas Paquetá', position: 'Meia', goals: 6 },
        { name: 'Marinho', position: 'Atacante', goals: 6 },
        { name: 'Thiago Galhardo', position: 'Meia', goals: 5 },
        { name: 'Luciano', position: 'Atacante', goals: 5 },
        { name: 'Hulk', position: 'Atacante', goals: 5 },
        { name: 'Vina', position: 'Meia', goals: 4 },
        { name: 'Rony', position: 'Atacante', goals: 4 },
        { name: 'Giorgian De Arrascaeta', position: 'Meia', goals: 4 },
        { name: 'Thiago Neves', position: 'Meia', goals: 4 },
        { name: 'Kaio Jorge', position: 'Atacante', goals: 4 },
        // Adicione mais jogadores aqui
      ]
    };
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
  width: 80%; /* Largura da tabela */
  border-collapse: collapse;
  margin: 0px; /* Espaço ao redor da tabela */
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

