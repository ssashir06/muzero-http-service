<template>
    <div id="app">
        <tic-tac-toe v-bind:seed="Math.floor(Math.random() * 10000)" />
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import TicTacToe from './components/TicTacToe.vue';

@Component({
    components: {
        TicTacToe,
    },
})
export default class App extends Vue {}
</script>

<style>

#app {
    font-family: cursive;
}

</style>
