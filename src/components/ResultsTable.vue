<template>
  <div class="round-table">
    <h2>{{ currentRound }}ª Rodada</h2>
    <div class="button-container">
    <button @click="previousRound">Rodada Anterior</button>
    <button @click="nextRound">Próxima Rodada</button>
    </div>
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
        <tr v-for="(match, index) in matches['Rodada' + currentRound]" :key="index">
          <td>{{ match.Local }}</td>
          <td>{{ match.Info_Jogo }}</td>
          <td>{{ match.Time1 }}</td>
          <td>{{ match.Placar }}</td>
          <td>{{ match.Time2 }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import jogosinfo from '../../jogos_rodada.json';

export default {
  name: 'RoundTable',
  data() {
    return {
      currentRound: 25, // Comece com a 27 rodada.
      matches: jogosinfo.jogosinfo,
    };
  },
  methods: {
    nextRound() {
      const roundKeys = Object.keys(this.matches);
      if (this.currentRound < roundKeys.length) {
        this.currentRound++;
      }
    },
    previousRound() {
      if (this.currentRound > 1) {
        this.currentRound--;
      }
    },
  },
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

.button-container {
  display: flex;
  justify-content: center;
  width: 80%; /* Alinhe a container de botões com a largura da tabela */
  margin-bottom: 10px; /* Adicione um espaço entre a container de botões e o título da rodada */
}

.button-container button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
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
