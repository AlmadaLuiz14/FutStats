<template>
    <div class="container">
      <div class="card">
        <h2>Alterar Jogador</h2>
        <form id="alterarJogador" @submit.prevent="alterarJogador">
          <div class="form-group label-float">
            <label for="nomeJog">Nome</label>
            <input
              class="form-control ls-login-bg-user input-lg"
              id="nomeJog"
              name="nomeJog"
              type="text"
              aria-label="Nome"
              placeholder="Nome"
              v-model="nomeJog"
              required
            />
  
            <label for="nick">Apelido</label>
            <input
              class="form-control ls-login-bg-user input-lg"
              id="nick"
              name="nick"
              type="text"
              aria-label="Apelido"
              placeholder="Apelido"
              v-model="nick"
            />
  
            <label for="time">Time</label>
            <input
              class="form-control ls-login-bg-user input-lg"
              id="time"
              name="time"
              type="text"
              aria-label="Time"
              placeholder="Time"
              v-model="time"
              required
            />
          </div>
          <p></p>
          <input
            type="submit"
            class="submit-btn"
            value="Enviar"
          />
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  
  export default {
    data() {
      return {
        nomeJog: null,
        nick: null,
        time: null,
      };
    },
  
    methods: {
      async alterarJogador() {
        try {
          // Envia os dados para o backend
          const altera_jogador = {
            nome: this.nomeJog,
            apelido: this.nick,
            time: this.time,
          };
  
          await axios.post(
            'http://localhost:5000/api/altera_jogador',
            altera_jogador
          );
  
          // Limpa os campos após o envio bem-sucedido
          this.nomeJog = null;
          this.nick = null;
          this.time = null;
  
          // Adicione qualquer lógica adicional após o envio bem-sucedido, se necessário
          alert('Jogador alterado com sucesso!');
        } catch (error) {
          // Exibe uma mensagem de erro
          console.error('Erro ao alterar jogador:', error);
          alert(
            'Erro ao alterar jogador. Verifique o console para mais detalhes.'
          );
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
        height: 43vh;
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