<template>            
    <div class='container'>
        <div>
            <h1 class="card">Cadastre-se e seja um</h1>
            <h1 class="card1">membro FutStats!</h1>

            <form id="cadastro" @submit.prevent="cadastrar">
                <div id='msgError'></div>
                <div id='msgSuccess'></div>
                
                <div class="label-float">
                    <label id="labelNome" for="nome">Nome</label>
                    <input type="text" id="nome" name="nome" v-model="nome" placeholder=" "  required>
                </div>
    
                <div class="label-float">
                    <label id="labelEmail" for="email">Email</label>
                    <input type="text" id="email" name="email" v-model="email" placeholder=" " required>
                </div>
                
                <div class="label-float">
                    <label id="labelSenha" for="senha">Senha</label>
                    <input type="password" id="senha" name="senha" v-model="senha" placeholder=" " required>
                    <i id="verSenha" class="fa fa-eye" aria-hidden="true"></i>
                </div>
    
                <div class="label-float confirme">
                    <label id="labelConfirmSenha" for="confirmSenha">Confirmar Senha</label>
                    <input type="password" id="confirmSenha" name="confirmSenha" v-model="confirmSenha" placeholder=" " @input="checarSenhas" required>
                    <i id="verConfirmSenha" class="fa fa-eye" aria-hidden="true"></i>
                </div>
                
                <div class='justify-center'>
                    <input type="submit" class="submit-btn" value="Cadastrar">
                    <p v-if="senhasDiferentes" class="verifSenhas">As senhas não coincidem</p>
                </div>
        
            </form>
        </div>
        <div class="additional-card1">
            <h2>Por que ser um membro FutStats?</h2>
            <p>Ao se juntar ao nosso grupo,</p> 
            <p>você terá acesso a notícias</p>
            <p>exclusivas</p>
            <p>sobre o Brasileirao, além de</p>
            <p> poder interagir comentando.</p>
            <img src="../assets/TrofeuLogo.png" alt="Troféu FutStats">
        </div>
    </div>
</template>

<script>
  import axios from 'axios';

  export default {
    nome: "usuarios",
    data() {
      return {
        nome: null,
        email: null,
        senha: null,
        confirmSenha: null,
        senhasDiferentes: false
      }
    },

    mounted(){
      const token = localStorage.getItem("UserToken")
      if(token !== null){window.location.replace("/")}
    },

    methods: {
      async cadastrar(e){
        if(this.checarSenhas() === false){
          e.preventDefault()
      
          const data = {
            email: this.email,
            nome: this.nome,
            senha: this.senha
          }

          try{
            const response = await axios.post("http://127.0.0.1:5000/api/usuario", data)
            console.log(response);

            alert("Cadastro realizado com sucesso!")
            this.$router.replace("/Login") //Se conseguir fazer logar automaticamente depois de cadastrar, mudar o replece para ("/")
          
          }catch(error){
            console.log("valor: ", error.status) //olhar essa verficação abaixo
            if (error['message'] === "Request failed with status code 501"){ //da pra melhorar isso daqui e pegar pelo código do erro
              alert("Este email já esta cadastrado")
              this.nome = ""
              this.email = ""
              this.senha = ""
              this.confirmSenha = ""
            }else{
              console.log(error);
              //console.log("Erro ao cadastrar", error);
            }
          }
        }
      },

      checarSenhas(){
        if(this.senha === this.confirmSenha){
          return this.senhasDiferentes = false
        }else{
          return this.senhasDiferentes = true
        }
      }
    }
  }

</script>


<style scoped>
.container {
  width: 60vw;
  height: 100vh;
  opacity: 0.93;
  background: #C0C0C0;
  padding: 25px;
  align-items: center;
  display: flex;
  justify-content: left;
}

.additional-card1 {
  width: 40vw;
  height: 100vh;
  background: #D8D8D8;
  position: absolute;
  left: 55.71vw;
  padding: 25px;
  text-align: center;
}
.card{
  position: absolute;
  top: 80px; /*240*/
  left: 250px; /*350*/
  font-family: 'Inter';
  font-size: 36px;
}
.card1{
  position: absolute;
  top: 120px;
  left: 277px;
  font-family: 'Inter';
  font-size: 36px;
}

.label-float {
  width: 80vh;
  height: 30px;
  top: 80px;
  left: 100px;
  position: relative;
  margin-bottom: 20px;
}

.label-float label {
  position: absolute;
  top: 0;
  left: 0;
  font-size: 16px;
  color: #333;
  pointer-events: none;
  transition: 0.2s ease all;
  padding-left: 5px;
}

.label-float input {
  width: 100%;
  padding: 5px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
  margin-top: 20px;
}

.submit-btn {
  background: #007BFF;
  color: #fff;
  font-size: 16px;
  padding: 10px 250px;
  margin-top: 195px;
  margin-left: 106px;
  margin-bottom: 100px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: 0.2s ease background-color;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.fa-eye {
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
}

.verifSenhas {
  color: red;
  font-size: 24px;
  margin-top: 10px;
  margin-left: 200px;
  text-align: center
}

.additional-card {
  height: 103vh;
  width: 76vh;
  top: 5.2vh;
  left: 126vh;
  padding: 15px;
  background: #D8D8D8;
  text-align: center;
  position: absolute;
}

.additional-card1 h2 {
  font-size: 40px;
  margin-bottom: 30px;
  font-family: 'Inter';
}

.additional-card1 p {
  font-size: 24px;
  margin-bottom: 10px;
  font-family: 'Inter';
}

.additional-card1 img {
  margin-top: 50px;
  max-width: 50%;
  height: auto;
}
</style>