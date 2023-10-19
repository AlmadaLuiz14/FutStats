<template>
  <div class="app">
  <nav class="header">
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
      </nav>
  
  
  <router-view/>
  </div>
</template>


<script>
  import TablesHome from './views/TablesHome.vue'
  import Login_screen from './views/Login_screen.vue'
  import Cad_screen from './views/Cad_screen.vue'

  export default{
    componets:{ TablesHome, 
                Login_screen,
                Cad_screen
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