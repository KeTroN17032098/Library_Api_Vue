<template>
    <div id="app">

    </div>
</template>


<script>
export default {
    mounted:{
        logcode(){
            console.log(this.$route.query.code)
        }
    }
}
</script>