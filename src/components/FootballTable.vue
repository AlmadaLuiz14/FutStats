<template>
  <div class="team-table">
    <p></p>
    <p></p>
    <h2>Tabela de Classificação</h2>
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Time</th>
          <th>Pontos</th>
          <th>Gols Marcados</th>
          <th>Gols Contra</th>
          <th>Saldo de Gols</th>
          <th>Jogos</th>
          <th>Vitórias</th>
          <th>Empates</th>
          <th>Derrotas</th>
          <th>Porcentagem de Vitórias</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(team, index) in tabela" :key="index">
          <td>{{ team.Classificação }}</td>
          <td>{{ team.Nome }}</td>
          <td>{{ team.Pontos }}</td>
          <td>{{ team['Gols Prós'] }}</td>
          <td>{{ team['Gols Contra'] }}</td>
          <td>{{ team['Saldo de Gols'] }}</td>
          <td>{{ team.Jogos }}</td>
          <td>{{ team.Vitórias }}</td>
          <td>{{ team.Empates }}</td>
          <td>{{ team.Derrotas }}</td>
          <td>{{ team['Porcentagem de Vitórias'] }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import tabela from '../../classificacao_brasileirao_2023.json';

export default {
  name: 'TeamTable',
  data() {
    // Use slice para remover os primeiros elementos (cabeçalho) do array
    const dadosSemCabecalho = tabela.tabela.slice(1);
    return {
      tabela: dadosSemCabecalho,
    };
  },
  methods: {
    // Os métodos calculateWinPercentage e calculateGoals permanecem os mesmos
    calculateWinPercentage(team) {
      if (team.Jogos === '0') {
        return '0.00%';
      }
      return ((team.Vitórias / team.Jogos) * 100).toFixed(2) + '%';
    },

    calculateGoals(team) {
      return team['Gols Prós'] - team['Gols Contra'];
    },
  },
};
</script>

<style scoped>
/* Estilos para centralizar a tabela na tela */


.team-table {
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
