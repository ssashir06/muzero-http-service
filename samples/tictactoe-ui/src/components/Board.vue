<template>
    <div class="board">
        <div class="row" v-for="row in 3" v-bind:key="row">
            <div class="col" v-for="col in 3" v-bind:key="col" @click="clicked(col-1, row-1)">
                <board-cell v-bind:value="valueFor(col-1, row-1)" />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import BoardCell from './BoardCell.vue';
import { cellValue } from './TicTacToe.vue';

type axis = 0|1|2;

@Component({
    components: {
        BoardCell,
    }
})
export default class Board extends Vue {
    // 3x3 matrix
    @Prop() private matrix!: cellValue[][] | null;

    private valueFor(x: axis, y: axis) {
        if (this.matrix == null) {
            return 0;
        } else {
            return this.matrix[x][y];
        }
    }

    private clicked(x: axis, y: axis) {
        this.$emit('action-clicked', x, y);
    }
}
</script>

<style scoped>

div.board {
    border: 2px solid black;
    padding: 0;
    margin: 0;
    display: table;
}
div.row {
    display: table-row;
    padding: 0;
    margin: 0;
}
div.col {
    border: 1px solid black;
    display: table-cell;
    vertical-align: middle;
    width: 100px;
    height: 100px;
    padding: 0;
    margin: 0;
    color: black;
    background-color: lightgray;
}

</style>