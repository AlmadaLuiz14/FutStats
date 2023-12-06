<template>
  <h1>
      {{ timeName }}
    </h1>
  <div class="time-screen">
    <div class="table-container">
      <h1>ELENCO</h1>
      <table>
        <thead>
          <tr>
            <th>Nome</th>
            <th>Apelido</th> 
          </tr>
        </thead>
        <tbody>
          <tr v-for="jogador in jogadores" :key="jogador.nome">
            <td>{{ jogador.nome }}</td>
            <td>{{ jogador.apelido }}</td>
          </tr>
        </tbody>
      </table>
      </div>
      
      <div class="table-container">
      <h1>ARTILHEIROS</h1>
      <table>
        <thead>
          <tr>
            <th>Apelido</th>
            <th>Gols</th> 
          </tr>
        </thead>
        <tbody>
          <tr v-for="jogador in artilheiros" :key="jogador.nome">
            <td>{{ jogador.apelido }}</td>
            <td>{{ jogador.gols }}</td> 
          </tr>
        </tbody>
      </table>
      </div>
      
      <div class="table-container">
      <h1>ASSISTÊNCIAS</h1>
      <table>
        <thead>
          <tr>
            <th>Apelido</th>
            <th>Assist</th> 
          </tr>
        </thead>
        <tbody>
          <tr v-for="jogador in assistencias" :key="jogador.nome">
            <td>{{ jogador.nome }}</td>
            <td>{{ jogador.assistencias }}</td> 
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      timeName: '',
      jogadores: [],
      artilheiros: [],
      assistencias: []
    };
  },
  created() {
    this.fetchTimeDetails();
  },
  methods: {
    normalizeTeamName(name) {
      const parts = name.split('-');
      if (parts.length > 1) {
        return parts.map(part => part.trim()).join('-');
      }
      return name.trim();
    },
    async fetchTimeDetails() {
      try {
        const time = this.$route.params.id;

        const response = await axios.get(`http://localhost:5000/api/time/${time}`);
        const response2 = await axios.get(`http://localhost:5000/api/artilheiros`);
        const response3 = await axios.get(`http://localhost:5000/api/assistencias`);

        if (!response.data || response.data.length === 0) {
          console.error('Dados da API vazios ou inválidos:', response.data);
          return;
        }

        if (!response2.data || response2.data.length === 0) {
          console.error('Dados da API vazios ou inválidos:', response2.data);
          return;
        }

        if (!response3.data || response3.data.length === 0) {
          console.error('Dados da API vazios ou inválidos:', response3.data);
          return;
        }

        console.log('Resposta da API:', response.data);
        console.log('Resposta da API:', response2.data);
        console.log('Resposta da API:', response3.data);

        this.timeName = this.normalizeTeamName(time);
        this.jogadores = response.data;
        this.artilheiros = response2.data
          .filter(jogadorArtilheiro => 
            this.jogadores.some(jogadorTime => 
              this.normalizeTeamName(jogadorTime.nome) === this.normalizeTeamName(jogadorArtilheiro.nome) ||
              this.normalizeTeamName(jogadorTime.apelido) === this.normalizeTeamName(jogadorArtilheiro.nome)
            )
          );
        this.assistencias = response3.data
          .filter(jogador => this.normalizeTeamName(jogador.time) === this.normalizeTeamName(time));
      } catch (error) {
        console.error('Erro ao buscar detalhes do time:', error);
      }
    },
  }
};
</script>


<style scoped>
  /* Estilos básicos para o componente time_screen.vue */
  .time-screen {
    margin: 20px;
    display: flex;
    
    justify-content: center;
  }

  h1 {
    font-size: 24px;
    color: #333;
  }

  .table-container {
    max-height: 80vh; /* Defina a altura máxima da tabela */
    overflow-y: auto; /* Adicione uma barra de rolagem vertical */
    margin: 20px;
  }

  /* Estilos para a tabela */
  table {
    border-collapse: collapse;
    margin-bottom: 10px; /* Espaço ao redor da tabela */
    width: 100%; /* Largura da tabela */
  }

  /* Estilos para as células da tabela */
  th, td {
    border: 1px solid #ddd; /* Borda de 1 pixel com cor cinza */
    padding: 8px;
    text-align: center;
    background-color: rgb(255, 255, 255, 0.5); /* Cor de fundo das linhas pares */
  }

  /* Estilos para as linhas ímpares da tabela */
  tr:nth-child(odd) {
    background-color: #f2f2f2; /* Cor de fundo das linhas ímpares */
  }
</style>
