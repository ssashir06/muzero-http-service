<template>
    <div class="board-cell">
        <p v-if="value<0">&#x26ab;</p>
        <p v-if="value>0">&#x2716;</p>
        <p v-if="value===0">&nbsp;</p>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { cellValue } from './TicTacToe.vue';

@Component
export default class BoardCell extends Vue {
    @Prop() private value!: cellValue;
}
</script>

<style scoped>
div.board-cell {
    text-align: center;
    font-size: 20pt;
}
</style>