<template>

<div id="userImg">
    <img :src="user.image" width=48 height=48>
    <p style="font-size:10px">Hello {{ user.name }}</p>
</div>

<div class="container">
    <div class="row">
        <div class="col-sm-10">
            <hr><br><br>
            <table class="table center paddingBetweenCols">
                <thead>
                    <tr>
                        <th scope="col"></th> <!-- For the image -->
                        <th scope="col">Artist</th>
                        <th scope="col">Album</th>
                        <th scope="col">Count</th>
                        <th></th>
                    </tr>
                </thead>
                
                <tbody>
                    <tr v-for="(album, index) in albums" :key="index">
                        <a :href="'https://open.spotify.com/album/' + album.id" target="_blank"><img :src="album.images[0].url" width=32 height=32></a>
                        <td>{{ toTitleCase(album.artist) }}</td>
                        <td>{{ toTitleCase(album.name) }}</td>
                        <td><strong style="font-size:25px;">{{ album.count }}</strong>/<strong style="font-size:10px;">{{ album.total_tracks }}</strong></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>
</template>

<script>
export default {
  name: 'PlaylistAlbums',
  data() {
    return {
        albums: [],
        user: {
            name: String,
            image: String
        }
    };
  },
  methods: {
    getUserInfo() {
        const path = "http://localhost:1312/user_info"
        fetch(path).then(response => response.json()).then(data => {this.user = data})
        console.log(this.user)
    },
    getAlbumsJson() {
        const path = "http://localhost:1312/albums";
        fetch(path).then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Something went wrong');
        })
        .then(responseJson => {this.albums = responseJson})
        .catch((error) => { console.error(error) });
    },
    toTitleCase(str) {
        return str.replace(/\w\S*/g, txt => {
            return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            }
        );
    }
  },
  beforeMount() {
    this.getUserInfo()
    this.getAlbumsJson()
  }
}
</script>

<style>
.center {
  margin-left: auto;
  margin-right: auto;
}
.paddingBetweenCols td {
  padding: 0 15px;
}
.userImg {
    text-align: left;
}
</style>