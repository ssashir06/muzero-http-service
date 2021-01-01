import axios from 'axios';
class ResponseInitialStep {
    observation!: number[][][];
    next!: number;
    legal!: number[];
}

class ResponseGameInfo {
    action_space!: number[];
    players!: number[];
}

class Action {
    number!: number;
    text!: string;
}

class Step {
    action!: number;
    root!: number | null;
    next!: number;
}

class ResponsePutAction {
    modelHash!: string;
    observation!: number[][][];
    next!: number;
    legal!: number[];
    action!: Action;
    done!: boolean;
    steps!: Step[];
}

type opponent = "human" | "random" | "expert" | "self";

export class MuZeroHttpService {
    private _seed: number;
    private _gameName: string;
    private _observation: number[][][] | null = null;
    private _actionSpace: number[] | null = null;
    private _players: number[] | null = null;
    private _nextPlayer: number | null = null;
    private _lastPlayer: number | null = null;
    private _legalActions: number[] = [];
    private _modelHash: string | null = null;
    private _steps: Step[] | null = null;
    private _done = true;
    private _gameover = true;
    private _status = "Not initialized";

    public constructor(seed: number, gameName: string) {
        this._seed = seed;
        this._gameName = gameName;
    }

    public get players() { return this._players; }
    public get nextPlayer() { return this._nextPlayer; }
    public get lastPlayer() { return this._lastPlayer; }
    public get gameover() { return this._gameover; }
    public get observation() { return this._observation; }
    public get legalActions() { return this._legalActions; }
    public get status() { return this._status; }

    public async reset() {
        // reset game
        const gameInfo = await axios.get<ResponseGameInfo>(
            `/game/${this._gameName}`
        ).then(ret => ret.data);
        this._actionSpace = gameInfo.action_space;
        this._players = gameInfo.players;

        // get initial state
        const step = await axios.get<ResponseInitialStep>(
            `/game/${this._gameName}/${this._seed}`
        ).then(ret => ret.data);
        this._nextPlayer = step.next;
        this._legalActions = step.legal;

        this._observation = null;
        this._steps = null;
        this._modelHash = null;
        this._done = false;
        this._gameover = false;
        this._lastPlayer = null;

        this._status = 'Game started.';
    }

    public async putAction(opponent: opponent, action: number | null) {
        let params = {};
        if (this._modelHash != null) {
            params = {
                ...params,
                'preffered_model_hash': this._modelHash,
            };
        }
        if (opponent == 'human') {
            if (action == null) {
                this._status = `Error: Action ${action} is not set.`;
                throw new Error(this._status);
            }
            if (!(this._actionSpace ?? []).includes(action)) {
                this._status = `Error: Action ${action} is invalid.`;
                throw new Error(this._status);
            }
            if (!this._legalActions.includes(action)) {
                this._status = `Error: Action ${action} is not allowed in this time.`;
                throw new Error(this._status);
            }
            params = {
                ...params,
                opponent: 'human',
                'human_action': action,
            };
        } else {
            params = {
                ...params,
                opponent,
                'human_action': action,
            };
        }

        const step = await axios.put<ResponsePutAction>(
            `/game/${this._gameName}/${this._seed}/action`,
            { steps: this._steps || [] }, { params }
        ).then(ret => ret.data);
        this._lastPlayer = this._nextPlayer;
        this._nextPlayer = step.next;
        this._modelHash = step.modelHash;
        this._observation = step.observation;
        this._legalActions = step.legal;
        this._steps = step.steps;
        this._done = step.done;

        this._gameover = this._done || this._legalActions.length == 0;
        this._status = this._gameover
            ? `Last action was "${step.action.text}" and game over!`
            : `Last action was "${step.action.text}"`;
    }

    public isLegal(action: number) {
        return this.legalActions.includes(action);
    }
}
