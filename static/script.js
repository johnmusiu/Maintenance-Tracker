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

showSlide(1); 

// toggle navbar for small screen devices by adding responsive class to navbar
function toggleNavbar(){
    const navbar = document.getElementById("topnav");
    if(navbar.className === "topnav"){
        navbar.classList.add("responsive");
    }else{
        navbar.classList.remove("responsive")
    }
}