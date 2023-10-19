<template>
  <div class="hello">
    <h2>{{ msg }}</h2>
    <div>
      <ul>
        <li v-for="(newsItem, index) in noticias.noticias" :key="newsItem.Título">
          <a :href="newsItem.Link" target="_blank">
            <div class="news-item">
              <!-- Verifique se não é a primeira notícia (index !== 0) antes de renderizar a imagem -->
              <img v-if="index !== 0" :src="newsItem.Imagem" alt="Imagem da Notícia" />
              <span>{{ newsItem.Título }}</span>
            </div>
          </a>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import noticias from '../../noticias_ge.json';

export default {
  name: 'NewsTable',
  props: {
    msg: String
  },
  data() {
    return {
      noticias
    };
  }
};
</script>

<style scoped>
.hello {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

h2 {
  margin: 0 0 20px;
  font-size: 24px;
  font-weight: bold;
}

ul {
  list-style-type: none;
  padding: 60px;
  background-color: rgb(255, 255, 255, 0.5); /* Cor de fundo das linhas pares */
  border-radius: 5px;
}

li {
  margin-bottom: 20px;
  display: flex;
  flex-direction: column; /* Altere para exibir os elementos em coluna */
  align-items: center; /* Centralize os elementos horizontalmente */
}

.news-item {
  display: flex;
  flex-direction: column; /* Altere para exibir os elementos em coluna */
  align-items: center; /* Centralize os elementos horizontalmente */
  text-align: center; /* Centralize o texto horizontalmente */
}

a {
  font-size: 36px;
  color: #000000;
  text-decoration: none;
  width: 150vh;
}

img {
  width: 120vh; /* Defina o tamanho da imagem de acordo com suas preferências */
  height: auto;
  margin-bottom: 10px; /* Adicione um espaço entre a imagem e o título */
  border-bottom: 1px solid #ccc; /* Linha separadora */
  padding-bottom: 120px; /* Espaço após a linha separadora */
}
</style>


