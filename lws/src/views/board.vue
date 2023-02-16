<template>
    <v-app id="app">
    <Myappbar></Myappbar>
    </v-app>
</template>

<script>
import Myappbar from '@/components/Myappbar.vue';
export default{
    data: () => ({
      cards: [
        { title: 'BlackList', src: 'http://localhost:8000/static/img/blacklist.png', flex: 12 ,link:''},
        { title: 'People Count', src: 'http://localhost:8000/static/img/count.jpg', flex: 12,link:''},
        { title: 'Thread', src: 'http://localhost:8000/static/img/sharedposts.png', flex: 12,link:''},
      ],
    }),
    component: {
        Myappbar: Myappbar,
    },
    components: { Myappbar }
}
</script>