<template>
  <div>
    <todo-header></todo-header>
    <v-parallax src="http://localhost:8000/static/img/bg.webp">
      <todo-content></todo-content>
    </v-parallax>
    <todo-footer></todo-footer>
  </div>
</template>

<script>
import TodoHeader from './components/TodoHeader.vue';
import TodoContent from './components/TodoContent.vue';
import TodoFooter from './components/TodoFooter.vue';

export default {
  data: function() {
    return {
      name: 'cslee'
    }    
  },
components: {
  'todo-header': TodoHeader,
  'todo-content': TodoContent,
  'todo-footer': TodoFooter,
}
}
</script>

<style>

</style>
