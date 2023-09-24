<template>
  <div class="table-container" v-if="notIsPageLogin && notIsPageCadastro">
    <nav class="header">
      <router-link to="/">Home</router-link>
      <router-link to= "/TabelaCampeonato" @click="scrollToSection('tabela-section')">Tabela</router-link>
      <router-link to="/Resultados" @click="scrollToSection('jogos-section')">Jogos</router-link>
      <router-link to="/Artilheiros" @click="scrollToSection('artilheiros-section')">Artilheiros</router-link>
      <router-link to="/Noticias" @click="scrollToSection('noticias-section')">Noticias</router-link>
      <div class="login">
        <router-link to="/Login">Login</router-link>
      </div>
      <div class="cadastro">
        <router-link to="/Cadastro">Cadastro</router-link>
      </div>
    </nav>
    <h1> Futstats </h1>
    <div logo>
      <img alt="Vue logo" src="./assets/TrofeuLogo.png" style="width: 350px">
    </div>
    <h1>Campeonato Brasileiro de Futebol</h1>
    <FootballTable msg=" TABELA "></FootballTable>
    <ResultsTable msg=" JOGOS "></ResultsTable>
    <TopsTable msg=" ARTILHEIROS "></TopsTable>
    <NewsTable msg=" NOTÍCIAS "></NewsTable>
    <LoginTe></LoginTe>
  </div>
</template>


<script>
import FootballTable from './components/FootballTable.vue'
import ResultsTable from './components/ResultsTable.vue'
import TopsTable from './components/TopsTable.vue'
import NewsTable from './components/NewsTable.vue'
import LoginTe from './components/LoginTe.vue'

export default {
  name: 'App',
  components: {
    FootballTable,
    ResultsTable,
    TopsTable,
    NewsTable,
    LoginTe
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
};
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
