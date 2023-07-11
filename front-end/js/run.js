function go(k) {
    $.get('http://192.168.50.1:5000/control/' + k, function () { });
}
$(function () {
    window.document.onkeydown = abc;
    function abc(env) {
        env = (env) ? env : window.event;
        if (env.keyCode == '87') {
            go('forward');
            $('#aup').css("color", "red")
        }
        if (env.keyCode == '83') {
            go('backward');
            $('#adown').css("color", "red")
        }
        if (env.keyCode == '65') {
            go('left');
            $('#aleft').css("color", "red")
        }
        if (env.keyCode == '68') {
            go('right');
            $('#aright').css("color", "red")
        }
    }
    window.document.onkeyup = qwe;
    function qwe(env) {
        env = (env) ? env : window.event;
        if (env.keyCode == '87') {
            $('#aup').css("color", "white")
        }
        if (env.keyCode == '83') {
            $('#adown').css("color", "white")
        }
        if (env.keyCode == '65') {
            $('#aleft').css("color", "white")
        }
        if (env.keyCode == '68') {
            $('#aright').css("color", "white")
        }
    }
    var i = null;
    $('#aup').mousedown(function () {
        i = setInterval(function () {
            go('forward');
        }, 100);
    });
    $('#aleft').mousedown(function () {
        i = setInterval(function () {
            go('left');
        }, 100);
    });
    $('#aright').mousedown(function () {
        i = setInterval(function () {
            go('right');
        }, 100);
    });
    $('#adown').mousedown(function () {
        i = setInterval(function () {
            go('backward');
        }, 100);
    });
    $('.box ul li').mouseup(function () {
        clearInterval(i);
    });
});