<template>
  <div class="table-container" v-if="notIsPageLogin && notIsPageCadastro">
    <nav class="header">
      <router-link to="/">Home</router-link>
      <router-link to= "/TabelaCampeonato" @click="scrollToSection('tabela-section')">Tabela</router-link>
      <router-link to="/Resultados" @click="scrollToSection('jogos-section')">Jogos</router-link>
      <router-link to="/Artilheiros" @click="scrollToSection('artilheiros-section')">Artilheiros</router-link>
      <router-link to="/Noticias" @click="scrollToSection('noticias-section')">Noticias</router-link>
      <div class="login">
        <router-link to="/Login" @click="toggleDivVisibility" >Login</router-link>
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
    <FootballTable id="tabela-section" msg=" TABELA "></FootballTable>
    <ResultsTable id="jogos-section" msg=" JOGOS "></ResultsTable>
    <TopsTable id="artilheiros-section" msg=" ARTILHEIROS "></TopsTable>
    <NewsTable id="noticias-section" msg=" NOTÍCIAS "></NewsTable>
  </div>
  <div class="table-container" v-if="notIsPagePrincipal">
    <nav class="header">
      <router-link to="/">Home</router-link>
    </nav>
    <LoginTe msg="Login"></LoginTe>
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
  data() {
    return {
      isVisible: false // Defina como true para que a div seja inicialmente visível
    };
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
    },
    toggleDivVisibility() {
      this.isVisible = !this.isVisible; // Alternar a visibilidade quando o botão for clicado
    }
  },
  computed: {
    notIsPagePrincipal(){
      return this.$route.name =="";
    },
    notIsPageLogin() {
      return this.$route.name !=="Login";
    },
    notIsPageCadastro() {
      return this.$route.name !=="Cadastro";
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
