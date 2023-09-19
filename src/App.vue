<template>
  <div logo>
    <img alt="Vue logo" src="./assets/TrofeuLogo.png" style="width: 950px">
  </div>
  <h1>Campeonato Brasileiro de Futebol</h1>
  <FootballTable msg =" TABELA "></FootballTable>
  <ResultsTable msg =" JOGOS "></ResultsTable>
  <TopsTable msg =" ARTILHEIROS "></TopsTable>
  <NewsTable msg =" NOTÍCIAS "></NewsTable>
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
  color: #2c3e50;
  margin-top: 60px;
}
</style>
