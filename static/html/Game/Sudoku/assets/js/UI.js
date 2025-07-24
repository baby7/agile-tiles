window.addEventListener("load", function(){

    // 全局常量
    BUTTONS = document.querySelector("#buttons > ul");
    BUTTONS_HOVER = document.getElementById("button-hover");
    SUDOKU_BOARD = document.getElementById("sudokuBoard");
    INPUTS = document.getElementsByTagName("input");
    LEFT = document.defaultView.getComputedStyle(BUTTONS_HOVER, null).left; // 按钮背景光的left偏移值
    OFFSET = 96; // 按钮背景光源移动的单位距离
    LEVELS = [33, 40, 50]; //难度等级
    LEVEL = LEVELS[0]; // 默认等级
    SHOW_SUDOKU = true; // 是否显示数独界面
    MESSAGE_CONTAINER = document.getElementById("message-container");
    BUTTON = document.getElementById("info-button");
    SUBMIT = document.getElementById("submit");


    //打开网页初始化
    generateSudoku(LEVEL);

    //按钮背景光源显示
    BUTTONS.addEventListener("mouseover", function(event){
        var li = event.target.parentNode;
        if(li.tagName.toLowerCase() == "li"){
            var i = 0;

            while(li = li.previousSibling){
                if(li.nodeType == 1) i += 1;
            }

            BUTTONS_HOVER.style.left = parseInt(LEFT) + OFFSET * i + "px";
            BUTTONS_HOVER.style.display = "block";
        }else{
            BUTTONS_HOVER.style.display = "none";
        }
    }, false);

    //按钮背景光消失
    BUTTONS.addEventListener("mouseleave", function(event){
        BUTTONS_HOVER.style.display = "none";
    }, false);

    //按钮点击事件触发相应事件
    BUTTONS.addEventListener("click", function(event){
        var link = event.target;
        if(link.tagName.toLowerCase() == "a"){
            switch(link.parentNode.id){
                case "refresh":
                    // sloveSudoku();
                    LEVEL = LEVELS[2];
                    generateSudoku(LEVEL);
                    break;
                case "level1":
                    LEVEL = LEVELS[0];
                    generateSudoku(LEVEL);
                    break;
                case "level2":
                    LEVEL = LEVELS[1];
                    generateSudoku(LEVEL);
                    break;
                case "level3":
                    LEVEL = LEVELS[2];
                    generateSudoku(LEVEL);
                    break;
                default:
                    break;
                    // toggleSudoku();
            }

            event.preventDefault();
        }
    }, false);

    // SUDOKU_BOARD.addEventListener('keyup', function(event){
    //     validateSudoku();
    // }, false);

    SUBMIT.addEventListener('click', function(){
        validateSudoku();
    }, false);

    BUTTON.addEventListener('click', function(){
        MESSAGE_CONTAINER.style.display = "none";
    }, false);

}, false);
