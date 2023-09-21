<template>
  <div class="team-table">
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
        <tr v-for="(team, index) in teamData" :key="index">
          <td>{{ index + 1 }}</td>
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
          name: 'Flamengo',
          points: 30,
          goalsScored: 35,
          goalsConceded: 15,
          gamesPlayed: 15,
          wins: 10,
          draws: 0,
          losses: 5
        },
        {
          name: 'Palmeiras',
          points: 28,
          goalsScored: 30,
          goalsConceded: 18,
          gamesPlayed: 15,
          wins: 9,
          draws: 1,
          losses: 5
        },
        {
          name: 'Atlético-MG',
          points: 27,
          goalsScored: 28,
          goalsConceded: 20,
          gamesPlayed: 15,
          wins: 8,
          draws: 3,
          losses: 4
        },
        {
          name: 'Fortaleza',
          points: 25,
          goalsScored: 22,
          goalsConceded: 18,
          gamesPlayed: 15,
          wins: 7,
          draws: 4,
          losses: 4
        },
        {
          name: 'Athletico-PR',
          points: 24,
          goalsScored: 20,
          goalsConceded: 17,
          gamesPlayed: 15,
          wins: 6,
          draws: 6,
          losses: 3
        },
        {
          name: 'São Paulo',
          points: 23,
          goalsScored: 24,
          goalsConceded: 20,
          gamesPlayed: 15,
          wins: 6,
          draws: 5,
          losses: 4
        },
        {
          name: 'Corinthians',
          points: 22,
          goalsScored: 20,
          goalsConceded: 19,
          gamesPlayed: 15,
          wins: 6,
          draws: 4,
          losses: 5
        },
        {
          name: 'Ceará',
          points: 21,
          goalsScored: 22,
          goalsConceded: 21,
          gamesPlayed: 15,
          wins: 6,
          draws: 3,
          losses: 6
        },
        {
          name: 'Internacional',
          points: 20,
          goalsScored: 18,
          goalsConceded: 19,
          gamesPlayed: 15,
          wins: 5,
          draws: 5,
          losses: 5
        },
        {
          name: 'Cuiabá',
          points: 19,
          goalsScored: 15,
          goalsConceded: 15,
          gamesPlayed: 15,
          wins: 4,
          draws: 7,
          losses: 4
        },
        {
          name: 'Juventude',
          points: 18,
          goalsScored: 17,
          goalsConceded: 18,
          gamesPlayed: 15,
          wins: 5,
          draws: 3,
          losses: 7
        },
        {
          name: 'Fluminense',
          points: 18,
          goalsScored: 16,
          goalsConceded: 18,
          gamesPlayed: 15,
          wins: 4,
          draws: 6,
          losses: 5
        },
        {
          name: 'Santos',
          points: 17,
          goalsScored: 15,
          goalsConceded: 20,
          gamesPlayed: 15,
          wins: 4,
          draws: 5,
          losses: 6
        },
        {
          name: 'Bahia',
          points: 16,
          goalsScored: 18,
          goalsConceded: 22,
          gamesPlayed: 15,
          wins: 4,
          draws: 4,
          losses: 7
        },
        {
          name: 'Grêmio',
          points: 15,
          goalsScored: 12,
          goalsConceded: 20,
          gamesPlayed: 15,
          wins: 3,
          draws: 6,
          losses: 6
        },
        {
          name: 'América-MG',
          points: 15,
          goalsScored: 13,
          goalsConceded: 16,
          gamesPlayed: 15,
          wins: 4,
          draws: 3,
          losses: 8
        },
        {
          name: 'Sport',
          points: 14,
          goalsScored: 14,
          goalsConceded: 19,
          gamesPlayed: 15,
          wins: 3,
          draws: 5,
          losses: 7
        },
        {
          name: 'Atlético-GO',
          points: 14,
          goalsScored: 13,
          goalsConceded: 21,
          gamesPlayed: 15,
          wins: 4,
          draws: 2,
          losses: 9
        },
        {
          name: 'Cruzeiro',
          points: 13,
          goalsScored: 14,
          goalsConceded: 30,
          gamesPlayed: 15,
          wins: 4,
          draws: 1,
          losses: 10
        },
        {
          name: 'Chapecoense',
          points: 12,
          goalsScored: 11,
          goalsConceded: 27,
          gamesPlayed: 15,
          wins: 3,
          draws: 3,
          losses: 9
        }
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
