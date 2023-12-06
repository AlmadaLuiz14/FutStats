<template>
  <div class="simula"></div>
    <div class="team-table">
      <p></p>
      <h2>Tabela de Classificação SIMULADA</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Time</th>
            <th>Pontos</th>
            <th>Jogos</th>
            <th>Vitórias</th>
            <th>Empates</th>
            <th>Derrotas</th>
            <th>Gols Marcados</th>
            <th>Gols Contra</th>
            <th>Saldo de Gols</th>
            <th>Porcentagem de Vitórias</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(team, index) in tabelaOrdenada" :key="index">
            <td style="text-align: center">
              {{ index+1}}º
            </td>
            <td>
              <router-link :to="{ name: 'time_screen', params: { id: team.nome } }">
              <img :src="team.brasao" alt="Brasão" class="team-logo" /> {{ team.nome }}
              </router-link>
            </td>
            <td style="text-align: center">{{ team.pontos }}</td>
            <td style="text-align: center">{{ team.jogos }}</td>
            <td style="text-align: center">{{ team.vitorias }}</td>
            <td style="text-align: center">{{ team.empates }}</td>
            <td style="text-align: center">{{ team.derrotas }}</td>
            <td style="text-align: center">{{ team.gols_pros }}</td>
            <td style="text-align: center">{{ team.gols_contra }}</td>
            <td style="text-align: center">{{ team.saldo_gols }}</td>
            <td style="text-align: center">{{ team.porcentagem_vitorias }}%</td>
          </tr>
        </tbody>
      </table>
      <div>
        <button @click="resetSimulation">Resetar Simulação</button>
        <button @click="exportToPDF">Exportar para PDF</button> 
      </div>
    </div>
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
            <th>Simular</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(match, index) in filteredMatches" :key="index">
            <td>{{ match.local }}</td>
            <td>{{ match.info_jogo }}</td>
            <td><img :src="match.brasao1" alt="Brasão" class="team-logo" /> {{ match.time1 }}</td>
            <td>{{ match.placar }}</td>
            <td>{{ match.time2 }}<img :src="match.brasao2" alt="Brasão" class="team-logo" /></td>
            <td class="input">
              <input
                v-model="input1[index]"
                style="width: 24px; height: 24px; text-align: center;"
              >
              X
              <input
                v-model="input2[index]"
                style="width: 24px; height: 24px; text-align: center;"
              >
              <button @click="simulateMatch(index)">Simular</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="select">
      <label for="selecao">Escolha uma tabela: </label>
      <select v-model="selecao" id="selecao">
        <option value="classificacao">Classificação</option>
        <option value="jogador">Jogador</option>
        <option value="rodadas">Rodadas</option>
      </select>
    </div>

    <div class="altera-table" v-if="time(this.selecao)">
      <inserir_time id="insereTime" msg="Inserção"></inserir_time>
      <alterar_time id="alterarTime" msg="Alteração"></alterar_time>
      <deletar_time id="deletaTime" msg="Remoção"></deletar_time>
    </div>

    <div class="altera-table" v-if="jogador(this.selecao)">
      <inserir_jog id="insereJog" msg="Inserção"></inserir_jog>
      <alterar_jog id="alterarJog" msg="Alteração"></alterar_jog>
      <deletar_jog id="deletaJog" msg="Remoção"></deletar_jog>
    </div>

    <div class="altera-table" v-if="rodada(this.selecao)">
      <inserir_rodada id="insereRod" msg="Inserção"></inserir_rodada>
      <alterar_rodada id="alterarRod" msg="Alteração"></alterar_rodada>
      <deletar_rodada id="deletaRod" msg="Remoção"></deletar_rodada>
    </div>
  <!--</div>-->
  </template>

<script>
import axios from 'axios';
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';
import inserir_time from './InsereTime.vue'
import alterar_time from './AlteraTime.vue'
import deletar_time from './DeletaTime.vue'
import inserir_jog from './InsereJogador.vue'
import alterar_jog from './AlteraJogador.vue'
import deletar_jog from './DeletaJogador.vue'
import inserir_rodada from './InsereRodada.vue'
import alterar_rodada from './AlteraRodada.vue'
import deletar_rodada from './DeletaRodada.vue'

pdfMake.vfs = pdfFonts.pdfMake.vfs;

export default {
  name: 'SimulateTables',

  components: {
    inserir_time,
    alterar_time,
    deletar_time,
    inserir_jog,
    alterar_jog,
    deletar_jog,
    inserir_rodada,
    alterar_rodada,
    deletar_rodada
  },

  data() {
    return {
      matches: [],
      tabela: [],
      currentRound: 38,
      round: 38,
      passado: false,
      input1: [],
      input2: [],
      timeName: '',
      jogadores: [],
      nomeDosTimes: {
      'ATH': { nome: 'Athletico Paranaense - PR', sigla: 'ATH' },
      'FLU': { nome: 'Fluminense - RJ', sigla: 'FLU' },
      'CUI': { nome: 'Cuiabá Saf - MT', sigla: 'CUI' },
      'SAO': { nome: 'São Paulo - SP', sigla: 'SAO' },
      'COR': { nome: 'Corinthians - SP', sigla: 'COR' },
      'FOR': { nome: 'Fortaleza - CE', sigla: 'FOR' },
      'INT': { nome: 'Internacional - RS', sigla: 'INT' },
      'SAN': { nome: 'Santos - SP', sigla: 'SAN' },
      'VAS': { nome: 'Vasco da Gama S.a.f. - RJ', sigla: 'VAS' },
      'BAH': { nome: 'Bahia - BA', sigla: 'BAH' },
      'CRU': { nome: 'Cruzeiro Saf - MG', sigla: 'CRU' },
      'GOI': { nome: 'Goiás - GO', sigla: 'GOI' },
      'COR-PR': { nome: 'Coritiba S.a.f. - PR', sigla: 'COR-PR' },
      'AME': { nome: 'América Saf - MG', sigla: 'AME' },
      'PAL': { nome: 'Palmeiras - SP', sigla: 'PAL' },
      'BOT': { nome: 'Botafogo - RJ', sigla: 'BOT' },
      'GRE': { nome: 'Grêmio - RS', sigla: 'GRE' },
      'RED': { nome: 'Red Bull Bragantino - SP', sigla: 'RED' },
      'ATL': { nome: 'Atlético Mineiro Saf - MG', sigla: 'ATL' },
      'FLA': { nome: 'Flamengo - RJ', sigla: 'FLA' },
    },

    selecao: null
    };
  },
  created() {
    this.initializeData();
  },
  computed: {
    filteredMatches() {
      return this.matches.filter((match) => parseInt(match.rodada) === this.currentRound);
    },
    tabelaOrdenada() {
  return this.tabela.slice().sort((a, b) => {
    if (b.pontos !== a.pontos) {
      return b.pontos - a.pontos; // Ordena por pontos descendentemente
    } else if (b.saldo_gols !== a.saldo_gols) {
      return b.saldo_gols - a.saldo_gols; // Ordena por saldo_gols descendentemente
    } else {
      return b.gols_pros - a.gols_pros; // Ordena por gols_pros descendentemente
    }
  });
},
  },
  methods: {

    time(select){
      if(select === "classificacao"){return true}else{return false}
    },
    
    jogador(select){
      if(select === "jogador"){return true}else{return false}
    },

    rodada(select){
      if(select === "rodadas"){return true}else{return false}
    },

    initializeData() {
      this.fetchClassificacao();
      this.fetchMatches();
      this.fetchTimeDetails();
      this.input1 = Array(this.matches.length).fill('');
      this.input2 = Array(this.matches.length).fill('');
    },
    normalizeTeamName(name) {
      return name.replace(/\s*-\s*/g, '-');
    },
    async fetchTimeDetails() {
  try {
    const siglaTime = this.$route.params.id;

    // Verifica se o nome da equipe está definido
    if (!siglaTime) {
      console.error("Nome da equipe não definido. A busca de detalhes do time será ignorada.");
      return;
    }

    // Mapeia a sigla para o nome completo usando o mapa
    const nomeCompletoTime = this.nomeDosTimes[siglaTime];

    // Verifica se a sigla corresponde a um nome completo conhecido
    if (!nomeCompletoTime) {
      console.error("Sigla do time desconhecida:", siglaTime);
      return;
    }

    const normalizedTime = this.normalizeTeamName(nomeCompletoTime);

    const response = await axios.get(
      `http://sua-api.com/api/time/${normalizedTime}`
    );

    this.timeName = normalizedTime;
    this.jogadores = response.data;
  } catch (error) {
    console.error("Erro ao buscar detalhes do time:", error);
  }
},
async fetchClassificacao() {
      try {
        const response = await axios.get('http://localhost:5000/api/simula');
        this.tabela = response.data.length > 1 ? response.data.slice(0) : response.data;
        this.fetchTimeDetails();
      } catch (error) {
        console.error('Erro ao buscar a tabela de classificação:', error);
      }
    },
    async fetchMatches() {
      try {
        const response = await axios.get('http://localhost:5000/api/jogos_simula');
        this.matches = response.data;
      } catch (error) {
        console.error('Erro ao buscar partidas:', error);
      }
    },
    nextRound() {
      if (this.currentRound < 38) {
        this.currentRound++;
      }
    },
    previousRound() {
      if (this.currentRound > 1) {
        this.currentRound--;
      }
    },

    recalculateRanking() {
      // Atualiza a classificação com base na nova ordem da tabela
      this.tabelaOrdenada.forEach((team, index) => {
        team.classificacao = index + 1;
      });
    },

    async simulateMatch(index) {
    const score1 = this.input1[index];
    const score2 = this.input2[index];

    const match = this.filteredMatches[index];
    
    console.log(`Rodada: ${match.rodada}, atual: ${this.round}`);

    // Verificar se a rodada da partida é maior ou igual à rodada atual
    if (parseInt(match.rodada) < this.round) {
      const userConfirmed = window.confirm('A rodada desta partida já passou. Gostaria mesmo de continuar com a simulação?');

      // Se o usuário não confirmar, pare a simulação
      if (!userConfirmed) {
          return;
      }
      
      this.passado = true;


    }

    console.log(`Simulação da Partida - Pontuação 1: ${score1}, Pontuação 2: ${score2}`);

    if (score1 < 0 || score2 < 0) {
        console.log(`Valores inválidos. Pontuação 1: ${this.filteredMatches[index].time1} ${score1}, Pontuação 2:${this.filteredMatches[index].time2}  ${score2}. A simulação será ignorada.`);
        return;
    }

    const numericScore1 = parseInt(score1);
    const numericScore2 = parseInt(score2);

    try {
        const match = this.filteredMatches[index];
        const sigla1 = match.time1;
        const sigla2 = match.time2;
        const time1 = this.nomeDosTimes[sigla1];
        const time2 = this.nomeDosTimes[sigla2];
        const placar = match.placar;

        // Simula a partida no front-end
        if (!this.passado){
          const simulatedData = this.simulateResults(time1, numericScore1, time2, numericScore2 );
          console.log('Dados simulados enviados para o backend:', simulatedData);
          alert('Simulação Efetuada com sucesso')
          // Envia os dados simulados para o backend
          await axios.post('http://localhost:5000/api/simula', simulatedData);
        }
        if (this.passado){
        const simulatedData = this.simulateResults2(time1, numericScore1, time2, numericScore2, placar );
        console.log('Dados simulados enviados para o backend:', simulatedData);
        alert('Simulação Efetuada com sucesso')
        // Envia os dados simulados para o backend
        await axios.post('http://localhost:5000/api/simula', simulatedData);
        }

        // Atualiza a tabela de classificação com os dados simulados
        await this.fetchMatches();
        await this.fetchClassificacao();

        this.recalculateRanking();

    } catch (error) {
        console.error('Erro ao simular a partida:', error);
    }
},

simulateResults(time1, score1, time2, score2) {
    const goalsFor1 = Math.max(score1, 0);
    const goalsAgainst1 = Math.max(score2, 0);
    const goalsFor2 = Math.max(score2, 0);
    const goalsAgainst2 = Math.max(score1, 0);
    const passado = this.passado;
    const placar1 = -1;
    const placar2 = -1;

    console.log('Cálculos de simulação - Time 1:', time1.nome);
    console.log('Gols a favor:', goalsFor1);
    console.log('Gols contra:', goalsAgainst1);

    console.log('Cálculos de simulação - Time 2:', time2.nome);
    console.log('Gols a favor:', goalsFor2);
    console.log('Gols contra:', goalsAgainst2);

    return {
        sigla1: time1.sigla,
        time1: time1,
        input1: score1,
        sigla2: time2.sigla,
        time2: time2,
        input2: score2,
        goalsFor1: goalsFor1,
        goalsAgainst1: goalsAgainst1,
        goalsFor2: goalsFor2,
        goalsAgainst2: goalsAgainst2,
        passado,
        placar1,
        placar2,
    };
},


simulateResults2(time1, score1, time2, score2, placar) {
    
    
    // Extrai os valores do placar
    const [valor1, valor2] = placar.split(' x ');

    // Converte os valores para inteiro
    const intValor1 = parseInt(valor1);
    const intValor2 = parseInt(valor2);

    const placar1 = intValor1;
    const placar2 = intValor2;

    // Calcula as diferenças
    const diff1 = intValor1 - Math.max(score1, 0);
    const diff2 = intValor2 - Math.max(score2, 0);

    // Atualiza os gols dos times
    const goalsFor1 = Math.max(score1, 0) + diff1;
    const goalsAgainst1 = Math.max(score2, 0);
    const goalsFor2 = Math.max(score2, 0) + diff2;
    const goalsAgainst2 = Math.max(score1, 0);

    const passado = this.passado;

    console.log('Cálculos de simulação - Time 1:', time1.nome);
    console.log('Gols a favor:', goalsFor1);
    console.log('Gols contra:', goalsAgainst1);

    console.log('Cálculos de simulação - Time 2:', time2.nome);
    console.log('Gols a favor:', goalsFor2);
    console.log('Gols contra:', goalsAgainst2);

    return {
        sigla1: time1.sigla,
        time1: time1,
        input1: score1,
        sigla2: time2.sigla,
        time2: time2,
        input2: score2,
        goalsFor1: goalsFor1,
        goalsAgainst1: goalsAgainst1,
        goalsFor2: goalsFor2,
        goalsAgainst2: goalsAgainst2,
        passado,
        placar1,
        placar2,
    };
},


async resetSimulation() {
    try {
      await axios.post('http://localhost:5000/api/reset-simulation');
      // Atualize a tabela de classificação após o reset
      await this.fetchClassificacao();
      await this.fetchMatches();
      this.recalculateRanking();
      this.passado = true;
      console.log('Simulação resetada com sucesso.');
      alert('Simulação Resetada')
    } catch (error) {
      console.error('Erro ao resetar a simulação:', error);
    }
  },

  exportToPDF() {
  // Adicione o cabeçalho da tabela
  const tabelaParaExportar = this.tabelaOrdenada;  // Ou qualquer tabela que você deseja exportar
  const headerRow = [
    { text: 'Classificação', bold: true },
    { text: 'Nome', bold: true },
    { text: 'Pontos', bold: true },
    { text: 'Jogos', bold: true },
    { text: 'Vitórias', bold: true },
    { text: 'Empates', bold: true },
    { text: 'Derrotas', bold: true },
    { text: 'Gols Prós', bold: true },
    { text: 'Gols Contra', bold: true },
    { text: 'Saldo de Gols', bold: true },
    { text: 'Porcentagem de Vitórias', bold: true },
  ];

  // Adicione os dados da tabela
  const content = [headerRow];
  tabelaParaExportar.forEach((row) => {
    const rowData = [
      { text: row.classificacao.toString() },
      { text: row.nome },
      { text: row.pontos.toString() },
      { text: row.jogos.toString() },
      { text: row.vitorias.toString() },
      { text: row.empates.toString() },
      { text: row.derrotas.toString() },
      { text: row.gols_pros.toString() },
      { text: row.gols_contra.toString() },
      { text: row.saldo_gols.toString() },
      { text: row.porcentagem_vitorias.toString() + '%' },
    ];
    content.push(rowData);
  });

  // Crie um objeto de definição PDF
  const pdfDefinition = {
    pageMargins: [20, 10, 20, 10], // Margens superior, direita, inferior e esquerda
    content: [
      { text: 'Tabela de Classificação', style: 'header' },
      { table: { body: content } },
    ],
    styles: {
      header: { fontSize: 18, bold: true, margin: [0, 0, 0, 10] },
    },
  };

  // Gere um Buffer com o conteúdo do PDF
  new Promise((resolve, reject) => {
    pdfMake.createPdf(pdfDefinition).getBuffer((buffer) => {
      resolve(buffer);
    }, (error) => {
      reject(error);
    });
  }).then((pdfBuffer) => {
    // Crie um Blob a partir do Buffer
    const pdfBlob = new Blob([pdfBuffer], { type: 'application/pdf' });

    // Crie um URL para o Blob
    const pdfUrl = URL.createObjectURL(pdfBlob);

    // Crie um link para download do PDF
    const link = document.createElement('a');
    link.href = pdfUrl;
    link.download = 'tabela_classificacao.pdf';

    // Adicione o link à página e clique nele para iniciar o download
    document.body.appendChild(link);
    link.click();

    // Remova o link da página
    document.body.removeChild(link);
  }).catch((error) => {
    console.error('Erro ao gerar o PDF:', error);
  });
},

// aqui termina o simulated
},
};
</script>
  
<style scoped>
/* Estilos para a tabela */

.simula{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh; /* Isso centraliza verticalmente na tela */
}

.team-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh; /* Isso centraliza verticalmente na tela */
  margin-bottom: 250px
}
.round-table {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  height: 100vh;
  margin-top: 200px;
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

.team-logo {
  width: 24px;
  height: 24px;
  margin-right: 8px;
  margin-left: 8px;
}

.input{
    display: flex;
    flex-direction:row;
    text-align: center;
}
</style>