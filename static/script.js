function toggleNavbar(){
    const navbar = document.getElementById("topnav");
    if(navbar.className === "topnav"){
        navbar.classList.add("responsive");
    }else{
        navbar.classList.remove("responsive")
    }
}