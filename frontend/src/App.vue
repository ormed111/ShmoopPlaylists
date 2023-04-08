<template>
  <h1 style="color:green">ShmoopPlaylists</h1>
  <UserInfo/>
  <PlaylistAlbums/>
  <GeneratePlaylist/>
</template>

<script>
import UserInfo from './components/UserInfo.vue'
import PlaylistAlbums from './components/PlaylistAlbums.vue'
import GeneratePlaylist from './components/GeneratePlaylist.vue'

export default {
  name: 'App',
  components: {
    UserInfo,
    PlaylistAlbums,
    GeneratePlaylist
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
