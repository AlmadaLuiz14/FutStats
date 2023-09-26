<template>
    <div class="coluna1">
        <h1 class="ls-login-logo">Login</h1>
        <form role="form">
                <div class="form-group ls-login-user">
                    <label for="userLogin">Usuário</label>
                    <input class="form-control ls-login-bg-user input-lg" id="userLogin" type="text" aria-label="Usuário" placeholder="Usuário">
                </div>
            
                <div class="form-group ls-login-password">
                    <label for="userPassword">Senha</label>
                    <input class="form-control ls-login-bg-password input-lg" id="userPassword" type="password" aria-label="Senha" placeholder="Senha">
                </div>

                <!--<a href="#" class="ls-login-forgot">Esqueci minha senha</a>-->

                <input type="submit" value="Entrar" class="btn btn-primary btn-lg btn-block">
                <p class="txt-center ls-login-signup">Não possui um usuário no FutStats?
                    <!--<a href="#">Cadastre-se agora</a>-->
                </p>
        </form>
    </div>
</template>

<script>
    import usuarios from '../db/db.json'

    export default{
        data(){
            return{
                form:{
                    email: null,
                    senha: null
                }
            }
        },

        methods:{
            login(){
                const user = usuarios.find(user => user.email === this.email)

                if(user && user.senha === this.senha){
                    alert("Login bem-sucedido!")
                }else{
                    alert("Não foi possível fazer o login")
                }
            }

        }
    }

</script>

<style>

    *,
    *::after,
    *::before{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        text-decoration: none;
    }

    .coluna1{
        margin-left: 0; 
    }

</style>