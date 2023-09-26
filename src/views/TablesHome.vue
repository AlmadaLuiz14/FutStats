<template>
    <div class="table-container inicio">
      <!--<nav class="header">
        <router-link to="/">Home</router-link>
        <router-link to= "/" @click="scrollToSection('tabela-section')">Tabela</router-link>
        <router-link to="/" @click="scrollToSection('jogos-section')">Jogos</router-link>
        <router-link to="/" @click="scrollToSection('artilheiros-section')">Artilheiros</router-link>
        <router-link to="/" @click="scrollToSection('noticias-section')">Noticias</router-link> 
        <div class="login">
          <router-link to="/Login">Login</router-link>
        </div>
        <div class="cadastro">
          <router-link to="/Cadastro">Cadastro</router-link>
        </div>
      </nav>-->
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
    },
    
    methods: {
      scrollToSection(sectionId) {
        const section = document.getElementById(sectionId);
        if (section) {
          window.scrollTo({
            top: section.offsetTop,
            behavior: 'smooth'
          });
        }
      }
    }
  }

  </script>
  
  
  <style scoped>
  
    .inicio{
      text-align: center;
    }

    /*#app {
      font-family: Avenir, Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
      color: #1c1c1c;
      margin-bottom: 0px; 
    }*/
  
  </style>
  