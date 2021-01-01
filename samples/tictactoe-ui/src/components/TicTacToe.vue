<template>
    <div class="tictactoe">
        <div class="content">
            <h1 class="title">
                Tic-Tac-Toe
            </h1>
        </div>
        <div class="content">
            <div class="board">
                <Board v-bind:matrix="matrix()" @action-clicked="clickingCell" />
            </div>
        </div>
        <div class="content">
            <div class="status">
                {{ this.muzero.status }}
            </div>
        </div>
        <div class="content">
            <div class="action" v-if="!muzero.gameover">
                <div>
                    Actions:
                </div>
                <div>
                    <span v-for="action in muzero.legalActions" v-bind:key="action">
                        <button @click="muzero.putAction('human', action)">
                            {{action}}
                        </button>
                    </span>
                </div>
                <div>
                    Computer:
                    </div>
                <div>
                    <button @click="muzero.putAction('self')">self</button>
                    <button @click="muzero.putAction('expert')">expert</button>
                    <button @click="muzero.putAction('random')">random</button>
                </div>
            </div>
        </div>
        <div class="content">
            <div class="start" v-if="muzero.gameover">
                <button @click="start()" >start</button>
                
                Seed:
                <input type="number" v-model="seed">
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { MuZeroHttpService } from '../models/muzero-http-service';
import Board from './Board.vue';

export type cellValue = 0 | 1 | -1;

@Component({
    components: {
        Board,
    }
})
export default class TicTacToe extends Vue {
    @Prop() private seed!: number;
    private muzero: MuZeroHttpService;

    public constructor() {
        super();
        this.muzero = new MuZeroHttpService(this.seed, "tictactoe");
    }

    private async mounted() {
        await this.muzero.reset();
    }

    private async start() {
        this.muzero = new MuZeroHttpService(this.seed, "tictactoe");
        this.seed = Math.floor(Math.random() * 10000);
        await this.muzero.reset();
    }

    private async clickingCell(x: number, y: number) {
        const action = y * 3 + x;
        if (!this.muzero.gameover && this.muzero.isLegal(action)) {
            await this.muzero.putAction('human', action)
        }
    }

    private matrix(): cellValue[][] | null {
        if (this.muzero.observation == null) {
            return null;
        } else {
            const arr = [
                Array(3),
                Array(3),
                Array(3),
            ];
            for (let row=0; row<3; row++) {
                for (let col=0; col<3; col++) {
                    if (this.muzero.observation[0][row][col] === 1) {
                        arr[col][row] = 1;
                    } else if (this.muzero.observation[1][row][col] === 1) {
                        arr[col][row] = -1;
                    } else {
                        arr[col][row] = 0;
                    }
                }
            }
            return arr;
        }
    }
}
</script>

<style scoped>
div.tictactoe {
    text-align: center;
    display: block;
}
div.content {
    display: block;
}
div.board {
    display: inline-block;
}
div.action, div.status, div.start {
    text-align: left;
    width: 300px;
    display: inline-block;
    border: 2px solid gray;
    padding: 5px;
    margin: 5px;
    border-radius: 10px;
}
button {
    padding: 7px;
    margin: 2px;
    border-radius: 10px;
}
</style>