//根据数组设置整个数独界面
function setSudokuUI(matrix){
    var element, childElement;

    for(var i=0; i<matrix.length; i++){
        element = document.getElementById(i);
        childElement = element.firstElementChild;
        if(childElement){
            if(childElement.tagName == "span"){
                childElement.removeChild(childElement.firstChild);
                if(matrix[i]){
                    childElement.appendChild(document.createTextNode(matrix[i]));
                }
            }else{
                childElement.value = matrix[i];
            }

        }else{
            if(matrix[i]){
                element.className = "staticValue";
                childElement = document.createElement('span');
                childElement.appendChild(document.createTextNode(matrix[i]));
            }else{
                element.className = "editValue";
                childElement = document.createElement('input');
                childElement.type = "text";
            }
            element.appendChild(childElement);
        }
    }
};

//生成数独界面
function generateSudoku(num){
    var element, childElement;
    var sudoku = new Sudoku();

    sudoku.initialize();
    sudoku.generate(num);

    // sudoku.showMatrix();

    for(var i=0; i<81; i++){
        element = document.getElementById(i);
        childElement = element.firstElementChild;
        if(childElement){
            element.removeChild(childElement);
        }

    }
    setSudokuUI(sudoku.matrix);
}

//从页面上获得数独对应的数据
function getMatrixFromTable(){
    var matrix = [], element, childElement, num;
    for(var i=0; i<81; i++){
        element = document.getElementById(i);
        childElement = element.firstElementChild;
        if(childElement.tagName.toLowerCase() == "span"){
            num = parseInt(childElement.firstChild.nodeValue);
            matrix.push(num);
        }else{
            if(childElement.value){
                matrix.push(parseInt(childElement.value));
            }else{
                matrix.push(0);
            }
        }
    }

    return matrix;
}

//根据数独信息破解数独并显示在页面上
function sloveSudoku(){
    var matrix = getMatrixFromTable();
    var sudoku = new Sudoku(matrix);

    matrix = sudoku.slove(sudoku.matrix);

    setSudokuUI(matrix);
}

function toggleAboutInfo(){
    $aboutInfo =  $('#about-info');
    if(SHOW_SUDOKU){
        $aboutInfo.animate({
            top: 100
        }, 8000);
    }else{
        $aboutInfo.css({top: '100%'});
    }
}

//数独消失
function toggleSudoku(){
    if(SHOW_SUDOKU){
        $("#sudokuBoard").animate({
            opacity: 0
        }, "slow");
        $('#sudokuBoard table').animate({
            borderSpacing: 15
        }, 'slow');
        toggleAboutInfo();
        SHOW_SUDOKU = false;
    }else{
        toggleAboutInfo();
        $('#sudokuBoard table').css({borderSpacing: 1});
        $('#sudokuBoard').css({opacity: 1});
        SHOW_SUDOKU = true;
    }
}

//判断数独是否完成与正确
function validateSudoku(){
    var matrix = getMatrixFromTable();

    var sudoku = new Sudoku(matrix);
    console.log("sudoku.getUnkownElements().length:{}", sudoku.getUnkownElements().length)

    if(sudoku.getUnkownElements().length == 0){
        console.log("start sudoku.validate")
        var message = sudoku.validate();
        console.log("end sudoku.validate")
        var messageContainer = document.getElementById("message-container");
        var messageInfo = document.getElementById("message-info");
        var classStyle = "error";
        if(!message){
            message = "矮油，不错哦！";
            // classStyle = "right";
        }
        messageInfo.className = classStyle;
        messageInfo.removeChild(messageInfo.firstChild);
        messageInfo.appendChild(document.createTextNode(message));
        messageContainer.style.display = "block";
    }
    else {
        var messageContainer = document.getElementById("message-container");
        var messageInfo = document.getElementById("message-info");
        var classStyle = "error";
        var message = "还有" + sudoku.getUnkownElements().length + "个空格未填";
        // messageInfo.className = classStyle;
        messageInfo.removeChild(messageInfo.firstChild);
        messageInfo.appendChild(document.createTextNode(message));
        messageContainer.style.display = "block";
    }
}
