'use strict';
function killAlert(){
    var alt = document.querySelectorAll('.alert')[0];
    alt.remove();
}

function setFunc(f1,f2){
    // if f1 returns true, execute f2
    if(f1()){
        f2();
    }
}

function checkAlert(){
    return document.getElementsByClassName('alert').length > 0;
}

setTimeout(function(){
    setFunc(checkAlert,killAlert);
},2500);

