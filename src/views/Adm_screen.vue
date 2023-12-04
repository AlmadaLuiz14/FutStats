<template>
    <div class="table">
        <h2>Tabela de Usuários</h2>
        <table>
            <thead>
                <tr>
                    <th>Nome</th>
                    <th>Email</th>
                    <th>Tornar Adm?</th>
                    <th>Tirar Adm?</th>
                    <th>Deletar?</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(user, index) in tabela" :key="index">
                    <td>{{  user.nome }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                        <button @click="tornaAdm(user.email)">Tornar Adm</button>
                    </td>
                    <td>
                        <button @click="tirarAdm(user.email)">Tirar Adm</button>
                    </td>
                    <td>
                        <button @click="deletarUser(user.email)">Deletar</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        data(){
            return{
                tabela: []
            };
        },

        created(){
            const token = localStorage.getItem("UserToken")
            const adm = localStorage.getItem("UserAdm")
                if((token === null) || (adm === null)){window.location.replace("/")}
                axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

            this.fetchUsers();
        },

        methods: {
            async fetchUsers(){
                try{
                    const response = await axios.get("http://127.0.0.1:5000/api/protegido/todosUsers")
                    this.tabela = response.data
                    
                }catch(error){
                    console.error("Erro ao buscar tabela de usuários", error)
                }
            },

            async deletarUser(email){
                const verify = window.confirm("Deseja realmente apagar esse usuário?")
            
                const data = {email: email}

                if(verify){
                    try{
                        const response = await axios.post("http://127.0.0.1:5000/api/protegido/deleteUser", data)
                        if(response.data.verify == true){
                            alert(response.data.msg)
                            window.location.reload()
                        }else{
                            alert(response.data.msg)
                        }
                    }catch(error){
                        console.error(error)
                    }
                }
            },

            async tornaAdm(email){
                const verify = window.confirm("Deseja realmente tornar esse usuário administrador?")
            
                const data = {email: email}

                if(verify){
                    try{
                        const response = await axios.post("http://127.0.0.1:5000/api/protegido/nAdm", data)
                        if(response.data.verify == true){
                            alert(response.data.msg)
                            window.location.reload()
                        }else{
                            alert(response.data.msg) 
                        }
                    }catch(error){
                        alert("Ocorreu um erro ao atualizar os adms")
                        console.error(error)
                    }
                }
            },

            async tirarAdm(email){
                const verify = window.confirm("Deseja realmente tirar esse usuário dos administradores?")
            
                const data = {email: email}

                if(verify){
                    try{
                        const response = await axios.post("http://127.0.0.1:5000/api/protegido/tirarAdm", data)
                        if(response.data.verify == true){
                            alert(response.data.msg)
                            window.location.reload()
                        }else{
                            alert(response.data.msg)
                        }
                    }catch(error){
                        alert("Ocorreu um erro ao atualizar os adms")
                        console.error(error)
                    }
                }
            }

        }
    }
</script>

<style scoped>
    .table {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh; /* Isso centraliza verticalmente na tela */
    }

    /* Estilos para a tabela */
    table {
    width: 80%; /* Largura da tabela */
    border-collapse: collapse;
    margin: 0px; /* Espaço ao redor da tabela */
    }

    /* Estilos para as células da tabela */
    th, td {
    border: 1px solid #ddd; /* Borda de 1 pixel com cor cinza */
    padding: 8px;
    text-align: left;
    background-color:  rgb(255, 255, 255, 0.5); /* Cor de fundo das linhas pares */
    }

    /* Estilos para as linhas ímpares da tabela */
    tr:nth-child(odd) {
    background-color: #f2f2f2; /* Cor de fundo das linhas ímpares */
    }

    /* Estilos para cabeçalho da tabela */
    th {
    background-color: #4CAF50; /* Cor de fundo para o cabeçalho */
    color: white; /* Cor do texto do cabeçalho */
    }
</style>