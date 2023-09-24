<template>
  <div class="table-container">
    <nav class="header">
      <router-link to="/">Home</router-link>
      <router-link to="/TabelaCampeonato">Tabela</router-link>
      <router-link to="/Resultados">Jogos</router-link>
      <router-link to="/Artilheiros">Artilheiros</router-link>
      <div class="login">
        <router-link to="/">Login</router-link>
      </div>
      <div class="cadastro">
        <router-link to="/">Cadastro</router-link>
      </div>
    </nav>
    <h1> Futstats </h1>
    <div logo>
      <img alt="Vue logo" src="./assets/TrofeuLogo.png" style="width: 350px">
    </div>
    <h1>Campeonato Brasileiro de Futebol</h1>
    <h1><br></h1>
    <FootballTable msg=" TABELA "></FootballTable>
    <ResultsTable msg=" JOGOS "></ResultsTable>
    <TopsTable msg=" ARTILHEIROS "></TopsTable>
    <NewsTable msg=" NOTÍCIAS "></NewsTable>
  </div>
</template>


<script>
import FootballTable from './components/FootballTable.vue'
import ResultsTable from './components/ResultsTable.vue'
import TopsTable from './components/TopsTable.vue'
import NewsTable from './components/NewsTable.vue'

export default {
  name: 'App',
  components: {
    FootballTable,
    ResultsTable,
    TopsTable,
    NewsTable
  }
}
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #1c1c1c;
  margin-bottom: 0px; 
}

.login{
  text-align: end;
  margin-top: -20px;
  margin-right: 100px;
}

.cadastro{
  text-align: end;
  margin-top: -18px;
  margin-right: 10px;
}

.header {
  background-color: #333;
  color: white;
  padding: 10px;
  text-align: center;
}


.header a {
  text-decoration: none;
  color: white;
  font-weight: bold;
  margin: 0 20px;
}

.header a:hover {
  text-decoration: underline;
  margin: 0 20px;
}

</style>
