<template>
  <div class="table-container inicio">
    <h1> Futstats </h1>
    <div logo>
      <img alt="Vue logo" src="../assets/TrofeuLogo.png" style="width: 350px">
    </div>
    <h1>Campeonato Brasileiro de Futebol</h1>
    <h1><br></h1>
    <FootballTable id="tabela-section" msg=" TABELA "></FootballTable>
    <ResultsTable id="jogos-section" msg=" JOGOS "></ResultsTable>
    <TopsTable id="artilheiros-section" msg=" ARTILHEIROS "></TopsTable>
    <NewsTable id="noticias-section" msg=" NOTÍCIAS "></NewsTable>
  </div>
</template>
  
  
  <script>
  import FootballTable from '../components/FootballTable.vue'
  import ResultsTable from '../components/ResultsTable.vue'
  import TopsTable from '../components/TopsTable.vue'
  import NewsTable from '../components/NewsTable.vue'
  
  export default {
    name: 'TablesHome',
    components: {
      FootballTable,
      ResultsTable,
      TopsTable,
      NewsTable
    }
  }
  </script>
  
  
  <style scoped>
  
    .inicio{
      text-align: center;
    }
  
  </style>
  