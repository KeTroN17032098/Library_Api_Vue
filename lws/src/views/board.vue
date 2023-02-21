<template>
    <v-app id="app">
        <Myappbar></Myappbar>
        <v-main>
            <v-container fluid class="bg-surface-variant" style="height: 100vh;" justify="center">
                <v-row>
                    <h1>Board</h1>
                    <v-spacer></v-spacer>
                    <v-btn variant="outlined" size="large" icon color="info">
                        <v-icon>mdi-pencil</v-icon>
                    </v-btn>
                </v-row>
                <v-row align="center" justify="center" child-flex>
                    <v-data-table-server 
                    :headers="headers"
                    :items="threads"
                    :loading="loading"
                    loading-text="Loading... Please wait"
                    :items-per-page="25" 
                    item-value="title" 
                    class="elevation-1"
                    hide-details>
                    </v-data-table-server>
                </v-row>
            </v-container>
        </v-main>
</v-app>
</template>

<script>

import Myappbar from '@/components/Myappbar.vue';
export default {
    data: () => ({
        headers:[
            {title:'Title',align:'start',sortable:'false',key:'title'},
            {title:'Created By',key:'created_by.email'},
            {title:'Created On',key:'created_on'},
            {title:'Comments Count',key:'comments_count'},
        ],
        loading:true,
        threads:[],
    }),
    component: {
        Myappbar: Myappbar,
    },
    components: { Myappbar },
    mounted() {
        this.$store.commit('getThreads', 1)
    },
}
</script>