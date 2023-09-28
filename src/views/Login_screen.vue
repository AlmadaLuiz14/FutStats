<template>
    <div class="container">
        <div class="card">
            <h1 class="ls-login-logo">Login</h1>
            <form id="login" @submit.prevent="login">
                <div class="form-group label-float">
                    <label for="userEmail">E-mail</label>
                    <input class="form-control ls-login-bg-user input-lg" id="userEmail" name="userEmail" type="text" aria-label="Usuário" placeholder="E-mail" v-model="email" required>
                </div>
            
                <div class="form-group label-float">
                    <label for="userPassword">Senha</label>
                    <input class="form-control ls-login-bg-password input-lg" id="userPassword" name="userPassword" type="password" aria-label="Senha" placeholder="Senha" v-model="senha" required>
                </div>

                <!--<a href="#" class="ls-login-forgot">Esqueci minha senha</a>-->

                <input type="submit" class="submit-btn" value="Entrar">
                <p class="txt-center ls-login-signup">Não possui um usuário no FutStats?
                    <!--<a href="#">Cadastre-se agora</a>-->
                </p>
            </form>
        </div>
    </div>
</template>

<script>

    export default {
        nome: "usuarios",
        data() {
            return {
                email: null,
                senha: null,
            }
        },

        methods: {
            async login(e){
                e.preventDefault()

                /*fetch("http://localhost:3000/usuarios")
                    .then(res => res.json())
                    .then(data => this.contas = data)
                    .catch(err => console.log(err.message))*/
                
                
                const data = await fetch("http://localhost:3000/usuarios", {
                    method: "GET",
                    headers: {"Content-Type": "application/json"}
                })
                
                const contas = await data.json()

                for(let i = 0; i < contas.length; i++){
                    if(contas[i]["email"] === this.email && contas[i]["senha"] === this.senha){
                        alert("Seja bem-vindo!")
                        break
                    }
                }


            }
        }
    }

</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.card {
  background: #d4d4d4;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 400px;
}

.label-float {
  position: relative;
  margin-bottom: 40px;
  margin-right: 35px;
  
}

.label-float label {
  position: absolute;
  left: 0;
  top: -24%;
  transform: translateY(-50%);
  pointer-events: none;
  transition: 0.3s ease-out all;
}

.label-float input {
  width: 100%;
  background: #dddddd;
  padding: 15px;
  font-size: 16px;
  border: 1px solid #000000;
  border-radius: 5px;
  outline: none;
}

.label-float input:focus {
  border-color: #007BFF;
}

.label-float input:not(:placeholder-shown) + label {
  top: 0;
  font-size: 12px;
  color: #007BFF;
}

.submit-btn {
  background-color: #007BFF;
  color: #fff;
  font-size: 16px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  transition: background-color 0.3s ease;
}

.submit-btn:hover {
  background-color: #0056b3;
}

.verSenha,
.verConfirmSenha {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.verifSenhas {
  color: red;
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}
</style>