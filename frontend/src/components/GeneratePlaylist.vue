<template>
  <div class="container">
    <button @click="onClick" type="button" class="btn btnGenerate" :disabled="generateInProgress">{{ buttonMsg }}
      <strong v-if="counter > 1" style="font-size:10px;">[take {{ counter }}]</strong>
    </button>

    <div v-if="generatedPlaylist.generated" class="generated" ref="playlist">
      <h3>Generated <a :href="generatedPlaylist.url" target="_blank">playlist</a> ({{ generatedPlaylist.tracks.length }} tracks):</h3>
      <text v-for="(track, index) in generatedPlaylist.tracks" :key="index">{{ index+1 }}. {{ track}}<br></text>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GeneratePlaylist',
  data() {
    return {
      buttonMsg: "Generate",
      generateInProgress: false,
      counter: 1,
      generatedPlaylist: {
        generated: false,
        tracks: [],
        url: ""
      }
    };
  },
  methods: {
    async onClick() {
      this.generatedPlaylist.generated = false
      this.generateInProgress = true
      this.buttonMsg = "Generating..."
      await this.generatePlaylist()
      this.generateInProgress = false
      this.generatedPlaylist.generated = true
      this.buttonMsg = "Generate"

      this.counter++
    },
    async generatePlaylist() {
        const path = "http://localhost:1312/generate"
        const response = await fetch(path)
        if (!response.ok) {
          throw new Error("Something went wrong with generate")
        }
        this.unpackGenerateResponse(await response.json())
    },
    unpackGenerateResponse(responseJson) {
      this.generatedPlaylist.tracks = responseJson.tracks;
      this.generatedPlaylist.url = responseJson.href;
    },
    scrollToPlaylist() {
      if (!this.generatedPlaylist.generated) {
        return
      }
      const el = this.$refs.playlist
      if (el) {
        el.scrollIntoView({behavior: 'smooth'})
      }
    }
  },
  updated() {
    this.scrollToPlaylist()
  }
};
</script>

<style>
.btnGenerate {
  background-color: #0ca761b1;
  border: none;
  color: white;
  padding: 16px 32px;
  text-align: center;
  font-size: 16px;
  margin: 4px 2px;
  opacity: 0.6;
  transition: 0.3s;
  display: inline-block;
  text-decoration: none;
  cursor: pointer;
}
.btnGenerate:hover {opacity: 1}

</style>