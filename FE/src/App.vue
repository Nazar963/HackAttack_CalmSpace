<script setup>
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
</script>


<template>
  <div id="app">
    <NavBar />
    <div>
  </div>
    <router-view></router-view>
  </div>
  <div id="app">
    <Footer />
  </div>
    <!-- <HelloWorld msg="Vite + Vue" /> -->
</template>


<style scoped>
/* Add any custom styles here */
</style>
