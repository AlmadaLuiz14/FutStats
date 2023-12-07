<template>
    <div class="container">
        <div class="card">
            <h2>Deletar Rodada</h2>
            <form id="novoTime" @submit.prevent="deletarTime">
                <div class="form-group label-float">
                    <label for="time1">Time Casa</label>
                    <input class="form-control ls-login-bg-user input-lg" id="time1" name="time1" type="text" aria-label="Time Casa" placeholder="Time Casa" v-model="time1" required>
                
                    <label for="time2">Time Visitante</label>
                    <input class="form-control ls-login-bg-user input-lg" id="time2" name="time2" type="text" aria-label="Time Visitante" placeholder="Time Visitante" v-model="time2" required>
                </div>
                <p></p>
                <input type="submit" class="submit-btn" value="Enviar">
            </form>
        </div>
    </div>
</template>

<script>

    export default {
        data() {
            return {
                time1: null, 
                time2: null
            }
        },

        methods: {
            async deletarTime(){
                console.log("Teste")
            }
        }
    }

</script>

<style scoped>

    .container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 39vh;
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