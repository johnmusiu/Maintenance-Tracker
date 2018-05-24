var index = 1;

function changeSlide(x){
    showSlide(index += x);
}

function currentSlide(x){
    showSlide(index = x);
}

function showSlide(x){
    var i;
    var slides = document.getElementsByClassName('slide');
    var dots = document.getElementsByClassName('dot');

    if(x > slides.length) { index = 1}
        if(x < 1) { index = slides.length }
        for(i = 0; i < slides.length; i++){
            slides[i].style.display = "none"
        }

        for(i = 0; i < dots.length; i++){
            dots[i].className = dots[i].className.replace(" active", "");
        }

    slides[index-1].style.display = "block";
    dots[index-1].className += " active";
}


// toggle navbar for small screen devices by adding responsive class to navbar

function toggleNavbar(){
    const navbar = document.getElementById("topnav");
    if(navbar.className === "topnav"){
        navbar.classList.add("responsive");
    }else{
        navbar.classList.remove("responsive")
    }
}

function toggleRequestForm(){
    const requestLink = document.getElementById("request-form");
    const requestDiv = document.getElementById("add-request");

    if(requestDiv.classList.contains('show-form')){
        requestDiv.classList.remove("show-form");
        requestDiv.classList.add("hide-form");
        requestLink.style.color = "white";
        requestLink.innerHTML = "Make Request";

    }else{
        requestLink.innerHTML = "Hide Request Form";
        requestDiv.classList.remove("hide-form");        
        requestDiv.classList.add("show-form");
    }    
}

showSlide(1); 
