<template>
  <div class="team-table">
    <h1>Tabela de Classificação</h1>
    <table>
      <thead>
        <tr>
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
        <tr v-for="(team, index) in teamData" :key="index">
          <td>{{ team.name }}</td>
          <td>{{ team.points }}</td>
          <td>{{ team.goalsScored }}</td>
          <td>{{ team.goalsConceded }}</td>
          <td>{{ calculateGoals(team) }}</td>
          <td>{{ team.gamesPlayed }}</td>
          <td>{{ team.wins }}</td>
          <td>{{ team.draws }}</td>
          <td>{{ team.losses }}</td>
          <td>{{ calculateWinPercentage(team) }}%</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'TeamTable',
  data() {
    return {
      teamData: [
        {
          name: 'Time A',
          points: 12,
          goalsScored: 15,
          goalsConceded: 8,
          gamesPlayed: 6,
          wins: 4,
          draws: 0,
          losses: 2
        },
        {
          name: 'Time B',
          points: 10,
          goalsScored: 12,
          goalsConceded: 10,
          gamesPlayed: 6,
          wins: 3,
          draws: 1,
          losses: 2
        },
        // Adicione mais times aqui
      ]
    };
  },
  methods: {
    calculateWinPercentage(team) {
      if (team.gamesPlayed === 0) {
        return 0;
      }
      return ((team.wins / team.gamesPlayed) * 100).toFixed(2);
    },

    calculateGoals(team) {
      if (team.gamesPlayed === 0) {
        return 0;
      }
      return (team.goalsScored - team.goalsConceded);
    }
  }
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
  margin: 20px; /* Espaço ao redor da tabela */
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
