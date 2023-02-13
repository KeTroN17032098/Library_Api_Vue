<template>
    <div id="app">
        <v-progress-circular indeterminate></v-progress-circular>
    </div>
</template>


<script>
import { toast } from 'vue3-toastify'
export default {
    data(){
        return{
            s:'s'
        }
    },
    mounted(){
        let provider=window.location.href.split('/')[4].split("?")[0]
        console.log(provider)
        let codedata={}
        codedata.code=this.$route.query.code
        codedata.state='STATE_STRING'
        this.$axios
            .post("http://localhost:8000/api/accounts/v1/sociallogin/SPA/"+provider+"/",JSON.stringify(codedata),{
                headers: {
                    "Content-Type": `application/json`,
                },
            })
            .then((res)=>{
                console.log(res.data.user.email)
                let payload = {}
                payload.userEmail = res.data.user.email
                payload.token = res.data.access_token
                payload.login_provider=provider
                this.$store.commit("login", payload)
            })
            .catch(error => {
                toast.error(error.request.responseText,{
                    autoClose:1000,

                })
            })
    }
}
</script>