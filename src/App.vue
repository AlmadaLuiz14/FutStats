<template>
  <router-view/>
</template>


<script>
  import TablesHome from './views/TablesHome.vue'
  import Login_screen from './views/Login_screen.vue'
  import Cad_screen from './views/Cad_screen.vue'

  export default{
    componets:{ TablesHome, 
                Login_screen,
                Cad_screen
    }
  }
</script>
