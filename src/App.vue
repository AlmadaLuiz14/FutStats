<template>
  <div class="app">
  <nav class="header">
        <router-link to="/">Home</router-link>
        <router-link to= "/" @click="scrollToSection('tabela-section')">Tabela</router-link>
        <router-link to="/" @click="scrollToSection('jogos-section')">Jogos</router-link>
        <router-link to="/" @click="scrollToSection('artilheiros-section')">Artilheiros</router-link>
        <router-link v-if="getToken" to="/" @click="scrollToSection('noticias-section')">Noticias</router-link>
        <router-link v-if="getToken" to="/Estatisticas">Estatísticas</router-link>
        <router-link v-if="getToken" to="/SimulaTable">Simulação</router-link>

        <div class="admin">
          <router-link v-if="getAdm" to="/Adm">Admin Config</router-link>
        </div>

        <div class="login">
          <router-link v-if="getToken" @click="logout" to="">Logout</router-link>
          <router-link v-else to="/Login">Login</router-link>
        </div>
        <div class="cadastro">
          <router-link v-if="getToken" to="/Usuario">Usuário</router-link>
          <router-link v-else to="/Cadastro">Cadastro</router-link>
        </div>
      </nav>
  
  <router-view/>
  </div>
</template>


<script>
  import TablesHome from './views/TablesHome.vue'
  import Login_screen from './views/Login_screen.vue'
  import Cad_screen from './views/Cad_screen.vue'
  import axios from 'axios'

  export default{
    componets:{ 
      TablesHome, 
      Login_screen,
      Cad_screen
    },
    
    computed: {
      getToken(){
        return localStorage.getItem("UserToken")
      },

      getAdm(){
        return localStorage.getItem("UserAdm")
      }

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

      logout(){
        localStorage.removeItem("UserToken")
        localStorage.removeItem("UserAdm")
        alert("LogOut feito com sucesso")
        //window.location.reload()
        window.location.replace("/")
      },

      async alertUser() {
        const token = localStorage.getItem('UserToken');
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}` 

        try{
          const response = await axios.get("http://127.0.0.1:5000/api/protegido")
          alert(response.data.nome)
        }catch(error){
          console.error(error)
        }
      }
    }

  }
</script>

<style scoped>

.admin{
    text-align: start;
    margin-top: -18px;
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