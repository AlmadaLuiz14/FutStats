<template>
    <head>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">  
    </head>
        <body>
            
            <div class='container'>
                <div class='card'>
                    <h1> Cadastrar </h1>
                    
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
            
                        <div class="label-float">
                            <label id="labelConfirmSenha" for="confirmSenha">Confirmar Senha</label>
                            <input type="password" id="confirmSenha" name="confirmSenha" v-model="confirmSenha" placeholder=" " @input="checarSenhas" required>
                            <i id="verConfirmSenha" class="fa fa-eye" aria-hidden="true"></i>
                        </div>
                        
                        <div class='justify-center'>
                            <!--<button onclick='cadastrar()'>Cadastrar</button>-->
                            <input type="submit" class="submit-btn" value="Cadastrar">
                            <p v-if="senhasDiferentes" class="verifSenhas">As senhas não coincidem</p>
                        </div>
                
                    </form>

                </div>
            </div>
            
        </body>
</template>

<script>

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

        methods: {
            async cadastrar(e){
                if(this.checarSenhas() === false){
                    e.preventDefault()
                    
                    const data = {
                        nome: this.nome,
                        email: this.email,
                        senha: this.senha
                    }

                    const dataJson = JSON.stringify(data)

                    const req = await fetch("http://localhost:3000/usuarios", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: dataJson
                    })

                    const res = await req.json()
                    res
                    //console.log(res)

                    this.nome = ""
                    this.email = ""
                    this.senha = ""
                    this.confirmSenha = "" 
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
</style>