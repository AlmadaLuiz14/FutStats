<template>
    <div class="container">
        <div class="card">
            <h2 class="perfil">Meu Perfil</h2>
            <h3>Deseja alterar suas informações?</h3>
            <form id="edit_infos" @submit.prevent="mudarInfos">
                <div class="form-group label-float">
                    <label for="userName">Nome</label>
                    <input class="form-control ls-login-bg-user input-lg" id="userName" name="userName" aria-label="Nome" :placeholder="placeHName" v-model="nome">
                </div>

                <div class="form-group label-float">
                    <label for="userEmail">Email</label>
                    <input class="form-control ls-login-bg-user input-lg" id="userEmail" name="userEmail" aria-label="Email" :placeholder="placeHEmail" v-model="email">
                </div>

                <div id="senha" class="form-group label-float">
                    <label for="userPass">Senha</label>
                    <input class="form-control ls-login-bg-user input-lg" id="userSenha" name="userSenha" type="password" aria-label="Senha" placeholder="Senha" v-model="senha" required>
                </div>

                <!--<div id="senhaC" class="form-group label-float">
                    <label for="userPassC">Confirmar Senha</label>
                    <input class="form-control ls-login-bg-user input-lg" id="userPassC" name="userPassC" aria-label="ConfirmarSenha" placeholder="Confirmar Senha" v-model="senhaC" required>
                </div>-->

                <input type="submit" class="submit-btn" value="Alterar Nome/Email">
            </form>

        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data() {
            return {
                placeHName: "",
                placeHEmail: "",
                nome: null,
                email: null,
                senha: null,
                //senhaC: null
            }
        },

        created() {
            try{
                const token = localStorage.getItem("UserToken")
                if(token === null){window.location.replace("/")}
                axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

                this.getEmailNome()
            }catch(error){
                console.error(error)
            }
        },

        methods: {
            async getEmailNome(){
                try{
                    const response = await axios.get("http://127.0.0.1:5000/api/protegido")
                    console.log(response.data.email)
                    this.placeHEmail = response.data.email.replace(/'/g, '')
                    this.placeHName = response.data.nome
                }catch(error){
                    console.error(error)
                }
            },

            async mudarInfos(){
                const data = {
                    nome: this.nome,
                    email: this.email,
                    senha: this.senha
                }

                if((this.nome !== null) && (this.email !== null)){

                    const verifSenha = await axios.post("http://127.0.0.1:5000/api/protegido/confereSenha", data)
                    if(verifSenha.data.verify === true){
                        const response = await axios.post("http://127.0.0.1:5000/api/protegido/newInfos", data)
                        alert(response.data.msg + ". Por ter alterado o email, por favor refaça seu login")
                        //Forçar o logout pra n dar erro por ter mudado o email
                        localStorage.removeItem("UserToken")
                        localStorage.removeItem("UserAdm")
                        window.location.replace("/Login")
                    }else{
                        alert("Senha incorreta")
                    }

                }else if(!((this.nome === null) && (this.email == null))){
                    if(this.nome === null){
                        data.nome = this.placeHName
                        const verifSenha = await axios.post("http://127.0.0.1:5000/api/protegido/confereSenha", data)
                        if(verifSenha.data.verify === true){
                            const response = await axios.post("http://127.0.0.1:5000/api/protegido/newInfos", data)
                            alert(response.data.msg + ". Por ter alterado o email, por favor refaça seu login")
                            //Forçar o logout pra n dar erro por ter mudado o email
                            localStorage.removeItem("UserToken")
                            localStorage.removeItem("UserAdm")
                            window.location.replace("/Login")
                        }else{
                            alert("Senha incorreta")
                        }
                    }else{
                        data.email = this.placeHEmail
                        const verifSenha = await axios.post("http://127.0.0.1:5000/api/protegido/confereSenha", data)
                        if(verifSenha.data.verify === true){
                            const response = await axios.post("http://127.0.0.1:5000/api/protegido/newInfos", data)
                            alert(response.data.msg)
                            window.location.reload()
                        }else{
                            alert("Senha incorreta")
                        }
                    }
                }
                this.senha = ''
                
                
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
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        text-align: center;
        max-width: 400px;
        width: 100%;
    }

    .card h2 {
        font-size: 1.5rem;
        margin-bottom: 10px;
    }

    .card h3 {
        font-size: 1rem;
        margin-bottom: 20px;
    }

    .form-group {
        margin-bottom: 20px;
        text-align: left;
    }

    .form-group label {
        display: block;
        font-size: 0.9rem;
        margin-bottom: 8px;
    }

    .form-group input {
        width: 95%;
        padding: 8px;
        font-size: 1rem;
        background: #dddddd;
        border: 1px solid #000000;
        border-radius: 4px;
        justify-content: center;
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
        justify-content: center;
    }

</style>