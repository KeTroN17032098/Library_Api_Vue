<template>
    <v-system-bar>
        <span class="ms-2">{{ this.time }}</span>
    </v-system-bar>
    <v-app-bar :elevation="2">
        <VAppBarTitle>Library Service</VAppBarTitle>
        <VSpacer></VSpacer>
        <v-menu open-on-hover close-on-content-click>
            <template v-slot:activator="{ props }">
                <v-btn icon="mdi-account" v-bind="props"></v-btn>
            </template>

            <v-card min-width="300">
                <v-list>
                    <v-list-item>
                        <v-list-item-title>{{ this.user_email }}</v-list-item-title>
                        <v-list-item-subtitle>logined via {{ this.user_provider }}</v-list-item-subtitle>
                    </v-list-item>
                </v-list>

                <v-divider></v-divider>

                <v-card-actions>
                    <v-spacer></v-spacer>

                    <v-btn color="primary" variant="text" @click="logout">
                        Logout
                    </v-btn>
                </v-card-actions>
            </v-card>

        </v-menu>
    </v-app-bar>
</template>

<script>



export default {
    data() {
        return {
            time: "",
            interval: null,
            user_email:"df",
            user_provider:"",
        }
    },
    mounted() {
        this.interval = setInterval(() => {
            this.time = Intl.DateTimeFormat(navigator.language, {
                hour: 'numeric',
                minute: 'numeric',
                second: 'numeric'
            }).format()
        }, 1000)
        this.user_email=this.$store.state.userStore.userEmail
        this.user_provider=this.$store.state.userStore.login_provider
    },
    beforeUnmount() {
        clearInterval(this.interval)
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
                            // ????????? ????????? ?????????????????? ??????
                            this.$store.commit("logout");
                        }
                    });
            }
            catch (error) {
                console.error(error);
            }
        },
    },
}
</script>