<template>
    <div class="container">
        <div class="card">
            <h2>Inserir Time</h2>
            <form id="novoTime" @submit.prevent="novoTime">
                <div class="form-group label-float">
                    <label for="nTimeNome">Nome</label>
                    <input class="form-control ls-login-bg-user input-lg" id="nTimeNome" name="nTimeNome" type="text" aria-label="Nome do Time" placeholder="Nome do Time" v-model="nome" required>
                    
                    <label for="brasao">Brasão</label>
                    <input class="form-control ls-login-bg-user input-lg" id="brasao" name="brasao" type="text" aria-label="Brasão do Time" placeholder="URL do Brasão" v-model="brasao" />
                    
                    <label for="ptsTimeNovo">Pontos</label>
                    <input class="form-control ls-login-bg-user input-lg" id="ptsTimeNovo" name="ptsTimeNovo" type="text" aria-label="Pontos do Time" placeholder="Pontos do Time" v-model="pts">
                
                    <label for="numJogos">Número de Jogos</label>
                    <input class="form-control ls-login-bg-user input-lg" id="numJogos" name="numJogos" type="text" aria-label="Número de Jogos" placeholder="Número de Jogos" v-model="numJogos">
                
                    <label for="numVit">Número de Vitórias</label>
                    <input class="form-control ls-login-bg-user input-lg" id="numVit" name="numVit" type="text" aria-label="Número de Vitórias" placeholder="Número de Vitórias" v-model="numVit">

                    <label for="numEmp">Número de Empates</label>
                    <input class="form-control ls-login-bg-user input-lg" id="numEmp" name="numEmp" type="text" aria-label="Número de Empates" placeholder="Número de Empates" v-model="numEmp">

                    <label for="numDer">Número de Derrotas</label>
                    <input class="form-control ls-login-bg-user input-lg" id="numDer" name="numDer" type="text" aria-label="Número de Derrotas" placeholder="Número de Derrotas" v-model="numDer">

                    <label for="gp">Número de Gols Feitos</label>
                    <input class="form-control ls-login-bg-user input-lg" id="gp" name="gp" type="text" aria-label="Número de Gols Feitos" placeholder="Número de Gols Feitos" v-model="gp">

                    <label for="gc">Número de Gols Tomados</label>
                    <input class="form-control ls-login-bg-user input-lg" id="gc" name="gc" type="text" aria-label="Número de Gols Tomados" placeholder="Número de Gols Tomados" v-model="gc">

                    <label for="cAmarelo">Número de Cartões Amarelos</label>
                    <input class="form-control ls-login-bg-user input-lg" id="cAmarelo" name="cAmarelo" type="text" aria-label="Número de Cartões Amarelos" placeholder="Número de Cartões Amarelos" v-model="cAmarelo">

                    <label for="cVermelho">Número de Cartões Vermelhos</label>
                    <input class="form-control ls-login-bg-user input-lg" id="cVermelho" name="cVermelho" type="text" aria-label="Número de Cartões Vermelhos" placeholder="Número de Cartões Vermelhos" v-model="cVermelho">
                </div>
                <p></p>
                <input type="submit" class="submit-btn" value="Enviar">
            </form>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        data() {
            return {
                nome: null,
                brasao: null,
                pts: null,
                numJogos: null,
                numVit: null,
                numEmp: null,
                numDer: null,
                gp: null,
                gc: null,
                sg: null,
                cAmarelo: null,
                cVermelho: null,
                porcentagem: null,
                temp: 0,
            }
        },

        methods: {
    async novoTime() {
      try {

        const valoresNumericos = [
          "pts",
          "numJogos",
          "numVit",
          "numEmp",
          "numDer",
          "gp",
          "gc",
          "sg",
          "cAmarelo",
          "cVermelho",
          "porcentagem",
        ];


        valoresNumericos.forEach((campo) => {
          this[campo] = this[campo] !== null ? Number(this[campo]) : null;
        });

        if (this.numJogos > 0){
            this.temp = this.numVit/this.numJogos
        }
        
        const novoTime = {
          nome: this.nome,
          brasao: this.brasao,
          pts: this.pts,
          numJogos: this.numJogos,
          numVit: this.numVit,
          numEmp: this.numEmp,
          numDer: this.numDer,
          gp: this.gp,
          gc: this.gc,
          sg: this.gp - this.gc,
          cAmarelo: this.cAmarelo,
          cVermelho: this.cVermelho,
          porcentagem: this.temp,
        };

        // Faça a requisição POST para a API
        await axios.post('http://localhost:5000/api/novo_time', novoTime);

        // Limpe os campos após o envio bem-sucedido
        this.nome = null;
        this.brasao = null;
        this.pts = null;
        this.numJogos = null;
        this.numVit = null;
        this.numEmp = null;
        this.numDer = null;
        this.gp = null;
        this.gc = null;
        this.cAmarelo = null;
        this.cVermelho = null;

        // Adicione qualquer lógica adicional após o envio bem-sucedido, se necessário
        window.location.reload();
        alert('Time inserido com sucesso!');
      } catch (error) {
        console.error('Erro ao inserir time:', error);
      }
    },
  },
};
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