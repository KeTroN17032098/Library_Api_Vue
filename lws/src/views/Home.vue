<template>
    <v-app id="app">
        <Myappbar></Myappbar>
        <v-main>
            <v-container fluid>
                <v-row dense>
                    <v-col v-for="card in cards" :key="card.title" :cols="card.flex">
                        <v-card>
                            <v-img :src="card.src" class="align-end"
                                gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.5)" height="400px" cover>
                                <v-card-title class="text-white" v-text="card.title"></v-card-title>
                            </v-img>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn  color="blue" variant="outlined" @click="card.link">Link</v-btn>
                                <v-spacer></v-spacer>
                            </v-card-actions>

                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-main>
    </v-app>
</template>

<script>
import Myappbar from '@/components/Myappbar.vue';
export default {
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
    methods: {
        logout() {
            try {
                this.$axios
                    .post("http://localhost:8000/api/accounts/v1/logout/", {
                        headers: {
                            "Content-Type": `application/json`,
                        },
                    })
                    .then((res) => {
                        if (res.status === 200) {
                            // 로그인 성공시 처리해줘야할 부분
                            this.$store.commit("logout");
                            this.$store.commit("loginCheck");
                        }
                    });
            }
            catch (error) {
                console.error(error);
            }
        },
    },
    components: { Myappbar }
};
</script>