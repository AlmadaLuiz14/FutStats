<template>
  <div class="round-table">
    <h1>{{ currentRound }}ª RODADA</h1>
    <div v-for="(match, index) in matches" :key="index" class="match">
      <div class="match-details">
        <p>{{ match.stadium }}</p>
        <p>{{ match.date }} {{ match.time }}</p>
      </div>
      <div class="teams">
        <p>{{ match.homeTeam }}</p>
        <p>{{ match.homeScore }}</p>
        <p>X</p>
        <p>{{ match.awayScore }}</p>
        <p>{{ match.awayTeam }}</p>
      </div>
    </div>
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
        }
        // Adicione mais partidas aqui
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
  
}

.match {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 80%;
  border: 1px solid #ddd;
  padding: 10px;
  margin: 10px;
  background-color: #f2f2f2; /* Cor de fundo das linhas ímpares */
}

.match-details {
  flex: 1;
}

.teams {
  flex: 2;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

/* Estilos para o cabeçalho */
h1 {
  text-align: center;
  font-size: 24px;
  margin-bottom: 10px;
}

/* Estilos para os detalhes do jogo */
p {
  margin: 0;
}

</style>
