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
                    <v-data-table v-model:items-per-page="itemsPerPage" :headers="headers" :items="desserts"
                        item-value="name" class="elevation-1"
                        hide-default-footer></v-data-table>
                </v-row>
            </v-container>
        </v-main>
</v-app>
</template>

<script>

import Myappbar from '@/components/Myappbar.vue';
export default {
    data: () => ({
        itemsPerPage: 5,
        headers: [
          {
            title: 'Dessert (100g serving)',
            align: 'start',
            sortable: false,
            key: 'name',
          },
          { title: 'Calories', align: 'end', key: 'calories' },
          { title: 'Fat (g)', align: 'end', key: 'fat' },
          { title: 'Carbs (g)', align: 'end', key: 'carbs' },
          { title: 'Protein (g)', align: 'end', key: 'protein' },
          { title: 'Iron (%)', align: 'end', key: 'iron' },
        ],
        desserts: [
          {
            name: 'Frozen Yogurt',
            calories: 159,
            fat: 6.0,
            carbs: 24,
            protein: 4.0,
            iron: '1',
          },
          {
            name: 'Jelly bean',
            calories: 375,
            fat: 0.0,
            carbs: 94,
            protein: 0.0,
            iron: '0',
          },
          {
            name: 'KitKat',
            calories: 518,
            fat: 26.0,
            carbs: 65,
            protein: 7,
            iron: '6',
          },
          {
            name: 'Eclair',
            calories: 262,
            fat: 16.0,
            carbs: 23,
            protein: 6.0,
            iron: '7',
          },
          {
            name: 'Gingerbread',
            calories: 356,
            fat: 16.0,
            carbs: 49,
            protein: 3.9,
            iron: '16',
          },
          {
            name: 'Ice cream sandwich',
            calories: 237,
            fat: 9.0,
            carbs: 37,
            protein: 4.3,
            iron: '1',
          },
          {
            name: 'Lollipop',
            calories: 392,
            fat: 0.2,
            carbs: 98,
            protein: 0,
            iron: '2',
          },
          {
            name: 'Cupcake',
            calories: 305,
            fat: 3.7,
            carbs: 67,
            protein: 4.3,
            iron: '8',
          },
          {
            name: 'Honeycomb',
            calories: 408,
            fat: 3.2,
            carbs: 87,
            protein: 6.5,
            iron: '45',
          },
          {
            name: 'Donut',
            calories: 452,
            fat: 25.0,
            carbs: 51,
            protein: 4.9,
            iron: '22',
          },
        ],
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