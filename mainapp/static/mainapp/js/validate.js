// Check and change color of tghe border bottom
function checkLength(x){
    if(x.value.length <= 4 ){
        x.style.border= "1px solid red";
    }

    if(x.value.length > 4 ){
        x.style.border = "1px solid green";
    }
}

function validatePassword(x){

    if(x.value.length < 4 ){
        x.style.border = "1px solid red";
    }

    if(x.value.length > 4 ){
        x.style.border = "1px solid green";
    }

    if(x.value != r_pass.value){
        r_pass_l.innerHTML = "Passwords do not match";
        r_pass_2_l.innerHTML = "Passwords do not match";
        r_pass_l.style.color = "red";
        r_pass_2_l.style.color = "red";
    }else{
        r_pass_l.innerHTML = "";
        r_pass_2_l.innerHTML = "Passwords match";
        r_pass_l.style.color = "green";
        r_pass_2_l.style.color = "green";
    }


}

var r_user = document.querySelector("#r_user");
var r_user_2 = document.querySelector("#r_user_2");

var l_user = document.querySelector("#l_user");
var l_user_2 = document.querySelector("#l_user_2");

var pass = document.querySelector("#pass");
var l_pass = document.querySelector("#l_pass");

var email = document.querySelector("#emai");
var r_emai = document.querySelector("#r_emai");

var pass_2 = document.querySelector("#pass_2");
var l_pass_2 = document.querySelector("#l_pass_2");

function validateForm(x){

    var errors = [];

    if(l_user.value.length < 4){
        l_user_2.innerHTML = "Must be at least 4 characters";
        errors = ["username"];
    }else{
        l_user_2.innerHTML = "";
    }


    if(pass.value.length < 5){
        l_pass.innerHTML = "Password Must be at least 5 characters";
        l_pass.style.color = "red";
        errors = ["email"];
    }else{
        l_pass.innerHTML = "";
    }

    if (errors.length >= 1){
         return false;
    }

}

function validateReg(x){

    var errors = [];

    if(r_user.value.length < 4){
        r_user_2.innerHTML = "Must be at least 4 characters";
        errors = ["username"];
    }else{
        r_user_2.innerHTML = "";
    }

    if(emai.value.length < 4){
        r_emai.innerHTML = "Enter a valid email";
        errors = ["emai"];
    }else{
        r_emai.innerHTML = "";
    }

    if(r_pass.value.length < 5){
        r_pass_l.innerHTML = "Password Must be at least 5 characters";
        r_pass_l.style.color = "red";
        errors = ["email"];
    }else{
        r_pass_l.innerHTML = "";
    }

    if (errors.length >= 1){
         return false;
    }

}

