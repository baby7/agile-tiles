function Sudoku(matrix){
    this.matrix = [];
    if(matrix){
        for(var i=0; i<81; i++){
            this.matrix[i] = matrix[i];
        }
    }else{
        for(var i=0; i<81; i++){
            this.matrix.push(0);
        }
    }
}

Sudoku.prototype = {
    constructor: Sudoku,

    showMatrix: function(){
        for(var i=0; i<9; i++){
            console.log(this.matrix.slice(i*9, (i+1)*9));
        }
    },

    getRowDigits: function(row){
        var start = row * 9;
        var arr = this.matrix.slice(start, start+9);
        arr.substract([0]);
        return arr;
    },

    getColDigits: function(col){
        var arr = [], i;
        for(i=0; i<9; i++){
            arr.push(this.matrix[i*9 + col]);
        }
        arr.substract([0]);
        return arr;
    },

    getSubMatrixDigits: function(num){
        var index = this.getIndexOfSubMatrix(num);
        var arr = [this.matrix[index], this.matrix[index+1], this.matrix[index+2],
                   this.matrix[index+9], this.matrix[index+10], this.matrix[index+11],
                   this.matrix[index+18], this.matrix[index+19], this.matrix[index+20]];
        arr.substract([0]);
        return arr;
    },

    getIndexOfSubMatrix: function(num){
        return Math.floor(num / 3) * 27 + (num % 3) * 3;
    },

    getCellAvailsList: function(cell){
        var row = Math.floor(cell / 9);
        var col = cell % 9;
        var box = Math.floor(row / 3) * 3 + Math.floor(col / 3);
        var avails = [1, 2, 3, 4, 5, 6, 7, 8 , 9];

        avails.substract(this.getRowDigits(row));
        avails.substract(this.getColDigits(col));
        avails.substract(this.getSubMatrixDigits(box));

        return avails;
    },

    fillNumber: function(cell){
        if(cell >= 81){
            return true;
        }else{
            var bool = false;
            var avails = Random.getRandomArray(this.getCellAvailsList(cell));
            if(avails.length == 0) return false;
            for(var i=0; i<avails.length; i++){
                this.matrix[cell] = avails[i];
                if(this.fillNumber(cell + 1)){
                    bool = true;
                    break;
                }
            }
            if(bool){
                return true;
            }else{
                this.matrix[cell] = 0;
                return false;
            }
        }
    },

    initialize: function(){
        this.fillNumber(0);
    },

    generate: function(num){
        var holes = Random.getRandomNumbers(0, 80, num);

        for(i=0; i<holes.length; i++){
            this.matrix[holes[i]] = 0;
        }
    },

    getUnkownElements: function(matrix){
        var arr=[], i;

        console.log("arguments:{}", arguments)
        if(arguments.length == 0) {
            matrix = this.matrix;
        }

        for(i=0; i<81; i++){
            if(matrix[i] == 0) arr.push(i);
        }

        return arr;
    },

    scan: function(matrix){

        do{
            var unkownArray = this.getUnkownElements(matrix);
            var min = 10;
            var change = false;
            var cell = null;
            var avails = [];

            for(var i=0; i<unkownArray.length; i++){
                avails = this.getCellAvailsList(unkownArray[i]);
                switch(avails.length){
                    case 0:
                        throw new ImpossibleError();
                        break;
                    case 1:
                        matrix[unkownArray[i]] = avails[0];
                        change = true;
                        break;
                    default:
                        if(avails.length < min){
                            min = avails.length;
                            cell = unkownArray[i];
                        }
                }
            }
        }while(change);

        return cell;
    },

    slove: function(matrix){
        matrix = matrix.slice(0);

        var cell = this.scan(matrix);

        if(cell === null) return matrix;

        var sudoku = new Sudoku(matrix);

        var avails = sudoku.getCellAvailsList(cell);

        for(var i=0; i<avails.length; i++){
            matrix[cell] = avails[i];

            try{
                return this.slove(matrix);
            }catch(ImpossibleError){
                continue;
            }
        }

        throw new (ImpossibleError);
    },

    validate: function(){
        console.log("validate:{}", "validate")
        var i, j, index;
        for(i=0; i<9; i++){
            var rowDigits = this.getRowDigits(i);
            var colDigits = this.getColDigits(i);
            var boxDigits = this.getSubMatrixDigits(i);
            console.log("rowDigits:{}", rowDigits)
            console.log("colDigits:{}", colDigits)
            console.log("boxDigits:{}", boxDigits)

            for(j=0; j<rowDigits.length; j++){
                index = rowDigits.lastIndexOf(rowDigits[j]);
                if(index != j) {
                    return ["在第", (i+1), "行的第", (j+1), "个数和第", (index+1), "个数冲突!"].join("");
                }
            }

            for(j=0; j<colDigits.length; j++){
                index = colDigits.lastIndexOf(colDigits[j]);
                if(index != j){
                    return ["在第", (i+1), "列的第", (j+1), "个数和第", (index+1), "个数冲突!"].join("");
                }
            }

            for(j=0; j<boxDigits.length; j++){
                index = boxDigits.lastIndexOf(boxDigits[j]);
                if(index != j){
                    return ["在第", (i+1), "个九宫格内的第", (j+1), "个数和第", (index+1), "个数冲突!"].join("");
                }
            }
        }

        return null;
    }
};





