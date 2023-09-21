const express = require('express');
const app = express();
const port = 3000;

// Define uma rota simples
app.get('/', (req, res) => {
  res.send('Hello, Express!');
});

// Inicia o servidor na porta especificada
app.listen(port, () => {
  console.log(`Servidor Express em execução na porta ${port}`);
});
