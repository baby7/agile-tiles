var Random = {

    //生成一个 small ~ big 之间的随机整数（包括 small 和 big）
    getRandomNumber: function(small, big){
        return small + Math.floor(Math.random() * (big - small + 1));
    },

    //small ~ big 之间随机取出 size 个组成一个数组
    getRandomNumbers: function(small, big, size){
        var start = big - size + 1;
        var arr = [];

        for(var i=start; i<=big; i++){
            var cur = this.getRandomNumber(small, i);
            var position = arr.indexOf(cur) + 1;
            var insert = position ? i : cur;

            arr.splice(position, 0, insert);
        }

        return arr;
    },

    //将数组元素顺序打乱
    getRandomArray: function(arr){
        var length = arr.length;
        var randomNumbers = this.getRandomNumbers(0, length-1, length);
        var newArr = [];

        for(var i=0; i<length; i++){
            newArr[i] = arr[randomNumbers[i]];
        }

        return newArr;
    }
};

//一个数组去除另一个数组中的所有元素
Array.prototype.substract = function(arr){
    for(var i=0; i<arr.length; i++){
        var index = this.indexOf(arr[i]);
        while(index != -1){
            this.splice(index, 1);
            index = this.indexOf(arr[i]);
        }
    }
};

//一个数组加上另一个数组中自己所没有的元素
Array.prototype.add = function(arr){
    for(var i=0; i<arr.length; i++){
        while(this.indexOf(arr[i]) == -1){
            this.push(arr[i]);
        }
    }
};

function ImpossibleError(){
    this.name = "ImpossibleError";
    this.message = "There is no answer for the sudoku!";
}


// 定义一个数独无法求解时的错误

ImpossibleError.prototype = new Error();



