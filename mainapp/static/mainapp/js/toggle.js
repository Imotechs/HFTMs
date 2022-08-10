
var sideBar = document.querySelector('#toggle-sidebar')
var contentBar = document.querySelector('nav')


var isClosed = true;
function togglesidebar(){
if(isClosed == true){
sideBar.className+="closed"
contentBar.className+="expand"
isClosed = false;
}
else{
    sideBar.className=""
contentBar.className=""
isClosed=true;
}




}

