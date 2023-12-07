<template>
    <div class="container">
        <div class="card">
            <h2>Deletar Time</h2>
            <form id="deletarTime" @submit.prevent="deletarTime">
                <div class="form-group label-float">
                    <label for="dTimeNome">Nome</label>
                    <input class="form-control ls-login-bg-user input-lg" id="dTimeNome" name="dTimeNome" type="text" aria-label="Nome do Time" placeholder="Nome do Time" v-model="nome" required>
                </div>
                <p></p>
                <input type="submit" class="submit-btn" value="Deletar">
            </form>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            nome: null
        };
    },

    methods: {
        async deletarTime() {
            try {
                // Construa um objeto com os dados do time a ser excluído
                const timeParaExcluir = {
                    nome: this.nome
                };

                // Faça a requisição POST para a nova rota de exclusão
                await axios.post('http://localhost:5000/api/deletar_time', timeParaExcluir);

                // Limpe os campos após a exclusão bem-sucedida
                this.nome = null;
                window.location.reload();
                alert('Time excluído com sucesso!');
            } catch (error) {
                console.error('Erro ao excluir time:', error);
            }
        }
    }
};
</script>

<style scoped>

    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 31vh;
    }

    .card {
        background: #d4d4d4;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        padding: 20px;
        width: 400px;
    }  

    .label-float label {
        position: absolute;
        left: 0;
        top: -20%;
        transform: translateY(-50%);
        pointer-events: none;
        transition: 0.3s ease-out all;
    }

    .label-float input {
        width: 92%;
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

</style>