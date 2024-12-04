<template>
  <div>
    <NavBar></NavBar>
    <AlertBox></AlertBox>
    <router-view></router-view>
  </div>
</template>

<script>
import AlertBox from './components/AlertBox.vue';
import NavBar from './components/NavBar.vue';

export default {
  name : 'App',
  components : {
    AlertBox,
    NavBar
  }
}
</script>