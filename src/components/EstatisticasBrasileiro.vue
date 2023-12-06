<template>
  <h2>Estatísticas Campeonato Brasileiro</h2> 
  <div class="est">
    <h2>Globais</h2>
    <table>
      <thead>
        <tr>
          <th>Descrição</th>
          <th>Dados</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in estatisticas.GLOBAIS" :key="key">
          <td>{{ key }}</td>
          <td>{{ value }}</td>
        </tr>
      </tbody>
    </table>

    <h2>Equipes</h2>
    <table>
      <thead>
        <tr>
          <th>Descrição</th>
          <th>Time</th>
          <th>Dados</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(teamData, key) in estatisticas.EQUIPES" :key="key">
          <td>{{ key }}</td>
          <td>{{ teamData.Time }}</td>
          <td>{{ getLastValue(teamData) }}</td>
        </tr>
      </tbody>
    </table>

    <h2>Jogadores</h2>
    <table class ='spa'>
      <thead>
        <tr>
          <th>Descrição</th>
          <th>Jogador</th>
          <th>Time</th>
          <th>Dados</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(playerData, key) in estatisticas.JOGADORES" :key="key">
          <td>{{ key }}</td>
          <td>{{ playerData.Jogador }}</td>
          <td>{{ playerData.Time }}</td>
          <td>{{ getLastValue(playerData) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <a href="https://www.cbf.com.br/stats/index.php?campeonato=42&amp;categoria=1&amp;exercicio=2023&amp;csrt=1569739546311501399" target="_blank" rel="noopener" class="btn">Ver EstatísticasCBF</a>
</template>
  
<script>
export default {
  data() {
    return {
      estatisticas: {
        GLOBAIS: {
            Jogos: "370",
            "Vitórias em Casa": "172 (46%)",
            "Jogos com -3 gols": "205 (55%)",
            Gols: "917",
            "Vitórias Fora": "101 (27%)",
            "Jogos com 3 ou mais gols": "165 (45%)",
            Média: "2,48",
            Empates: "97 (26%)",
            "Resultado Típico": "1-0 (49 J)",
        },
        EQUIPES: {
          "Melhor Ataque": { Time: "Palmeiras", Gols: "63" },
          "Pior Ataque": { Time: "Cruzeiro", Gols: "34" },
          "Melhor Defesa": { Time: "Atlético Mineiro", "Gols Sofridos": "28" },
          "Pior Defesa": { Time: "América Mineiro", "Gols Sofridos": "80" },
          "Mais Goleadas": { Time: "Palmeiras", Goleadas: "6" },
          "Mais Vitórias": { Time: "Grêmio +1", Vitórias: "20" },
          "Menos Vitórias": { Time: "América Mineiro", Vitórias: "5" },
          "Mais Empates": { Time: "Corinthians +1", Empates: "14" },
          "Menos Empates": { Time: "Grêmio", Empates: "5" },
          "Mais Derrotas": { Time: "Coritiba +1", Derrotas: "23" },
          "Menos Derrotas": { Time: "Palmeiras", Derrotas: "8" },
          "Max. Jogos sem Perder": { Time: "Botafogo", Jogos: "12" },
          "Mais Amarelos": { Time: "Coritiba", Amarelos: "122" },
          "Mais Vermelhos": { Time: "América Mineiro", Vermelhos: "8" },
          "Mais Gols Contra a Favor": { Time: "Cruzeiro", Gols: "3" },
        },
        JOGADORES: {
          Artilheiro: { Jogador: "Paulinho", Time: "Atlético Mineiro", Gols: "19" },
          "Mais Assistências": { Jogador: "Luis Suárez +1", Time: "Grêmio", Assistências: "11" },
          "Participação em Gols": { Jogador: "Luis Suárez +1", Time: "Grêmio", "Gols/Assistências": "26" },
          "Média de Gols/Jogo": { Jogador: "Alan", Time: "Fluminense", "Gols/Jogo": "1.00" },
          "Mais Gols de Pênalti": { Jogador: "Robson", Time: "Coritiba", Gols: "7" },
          "Mais gols como reserva": { Jogador: "Yago Pikachu", Time: "Fortaleza", Gols: "5" },
          "Gols de Vitória": { Jogador: "Paulinho", Time: "Atlético Mineiro", Gols: "6" },
          "Dois gols em um jogo": { Jogador: "Tiquinho Soares", Time: "Botafogo", Jogos: "4" },
          "Três gols em um jogo": { Jogador: "Luis Suárez +1", Time: "Grêmio", Jogos: "1" },
          "Mais Amarelos": { Jogador: "Wálter Kannemann", Time: "Grêmio", Amarelos: "16" },
          "Mais Segundos Amarelos": { Jogador: "Lucas Oliveira +1", Time: "Cruzeiro", "Segundos Amarelos": "2" },
          "Mais Vermelhos": { Jogador: "Nino +3", Time: "Fluminense", Vermelhos: "2" },
          "Mais Minutos": { Jogador: "Cássio", Time: "Corinthians", Minutos: "3330" },
          "12º Jogador": { Jogador: "Thiago Borbas", Time: "Red Bull Bragantino", "Jogos como reserva utilizado": "22" },
          "Mais Gols Sofridos": { Jogador: "Gabriel Vasconcellos", Time: "Coritiba", "Gols Sofridos": "60" },
        },
      },
    };
  },
  methods: {
    getLastValue(obj) {
      // Obtém a última propriedade não nula/undefined do objeto
      const lastValue = Object.values(obj).reverse().find((val) => val !== undefined && val !== null);
      return lastValue !== undefined ? lastValue : 'N/A';
    },
  },
};
</script>
  
  
  <style scoped>
  .est{
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  table {
    border-collapse: collapse;
    width: 40%; /* Largura da tabela */ 
    margin-bottom: 40px;
  }

  .spa{
    margin-bottom: 100px;
  }

  /* Estilos para as células da tabela */
  th, td {
    border: 1px solid #ddd; /* Borda de 1 pixel com cor cinza */
    padding: 5px;
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