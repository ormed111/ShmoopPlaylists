<template>
    <div id="userImg">
        <img v-if="user.image" :src="user.image" width=48 height=48>
        <p v-if="user.name" style="font-size:10px">Hello {{ user.name }}</p>
    </div>
</template>

<script>
export default {
  name: 'UserInfo',
  data() {
    return {
        user: {
            name: "",
            image: ""
        }
    };
  },
  methods: {
    getUserInfo() {
        const path = "http://localhost:1312/user_info"
        fetch(path).then(response => response.json()).then(data => {this.user = data})
        console.log(this.user)
    }
  }, 
  created() {
        this.getUserInfo()
    }
  
}

</script>

<style>
.userImg {
    text-align: left;
}
</style>