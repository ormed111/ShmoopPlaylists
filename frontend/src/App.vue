<template>
  <h1 style="color:green">ShmoopPlaylists</h1>
  <PlaylistAlbums/>
</template>

<script>
import PlaylistAlbums from './components/PlaylistAlbums.vue'

export default {
  name: 'App',
  components: {
    PlaylistAlbums
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  background-color: #ddedbf;
}
</style>
