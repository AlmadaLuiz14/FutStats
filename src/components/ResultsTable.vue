<template>
  <div class="round-table">
    <p></p>
    <p></p>
    <h2>{{ currentRound }}ª Rodada</h2>
    <table>
      <thead>
        <tr>
          <th>Estádio</th>
          <th>Data e Hora</th>
          <th>Time da Casa</th>
          <th>Placar</th>
          <th>Time Visitante</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(match, index) in matches" :key="index">
          <td>{{ match.stadium }}</td>
          <td>{{ match.date }} {{ match.time }}</td>
          <td>{{ match.homeTeam }}</td>
          <td>{{ match.homeScore }} - {{ match.awayScore }}</td>
          <td>{{ match.awayTeam }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>


<script>
export default {
  name: 'RoundTable',
  data() {
    return {
      currentRound: 23, // Rodada atual
      matches: [
        {
          stadium: 'Kleber Andrade',
          date: '13/09',
          time: '21:30',
          homeTeam: 'Flamengo',
          homeScore: 0,
          awayScore: 3,
          awayTeam: 'Athletico-PR'
        },
        {
          stadium: 'Beira-Rio',
          date: '13/09',
          time: '21:30',
          homeTeam: 'Internacional',
          homeScore: 2,
          awayScore: 1,
          awayTeam: 'São Paulo'
        },
        {
          stadium: 'Vila Belmiro',
          date: 'Hoje',
          time: '19:00',
          homeTeam: 'Santos',
          homeScore: null,
          awayScore: null,
          awayTeam: 'Cruzeiro'
        },
        {
          stadium: 'Maracanã',
          date: '14/09',
          time: '20:00',
          homeTeam: 'Fluminense',
          homeScore: null,
          awayScore: null,
          awayTeam: 'Grêmio'
        },
        {
          stadium: 'Mineirão',
          date: '14/09',
          time: '20:30',
          homeTeam: 'Atlético-MG',
          homeScore: null,
          awayScore: null,
          awayTeam: 'Bahia'
        },
        {
          stadium: 'Arena Fonte Nova',
          date: '15/09',
          time: '19:15',
          homeTeam: 'Vitória',
          homeScore: null,
          awayScore: null,
          awayTeam: 'Corinthians'
        },
        {
          stadium: 'Arena Castelão',
          date: '15/09',
          time: '21:30',
          homeTeam: 'Fortaleza',
          homeScore: null,
          awayScore: null,
          awayTeam: 'Palmeiras'
        },
        {
          stadium: 'Estádio Nilton Santos',
          date: '16/09',
          time: '20:00',
          homeTeam: 'Botafogo',
          homeScore: null,
          awayScore: null,
          awayTeam: 'Flamengo'
        },
        {
          stadium: 'Arena da Baixada',
          date: '16/09',
          time: '21:00',
          homeTeam: 'Athletico-PR',
          homeScore: null,
          awayScore: null,
          awayTeam: 'Internacional'
        }
      ]
    };
  }
};
</script>

<style scoped>
/* Estilos para a tabela */
.round-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  height: 100vh;
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
