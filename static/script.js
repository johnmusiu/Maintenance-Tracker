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


function toggleRequestDetails(id){
    //get table on page by htmltag, 0 gets obj of the first table in the page
    const table = document.getElementsByTagName("table")[0];
    // from table obj get tr rows list
    const rows = table.getElementsByTagName("tr"); // 
    //loop through rows list
    for(var i = 1; i < rows.length; i++){
        // row object
        var row = rows[i];
        // Track with onclick(a row with a clicked event will trigger this)
        row.onclick = function(){
            var rowIndex = this.rowIndex;
            insertDescRow(table, rows, rowIndex, id);            
        }
    }
}

//create row for request description
function insertDescRow(table, rows, rowIndex, id){
    const row = rows[rowIndex];
    console.log((rowIndex+1)+" "+rows.length)
    //if not last row, check if row should be added or deleted
    if(rows.length !== rowIndex+1){
        const nextRow = rows[rowIndex+1];
        if(nextRow.classList.contains("shown")){
            //delete that row
            table.deleteRow(rowIndex+1);
            stop();
        }else{
            createRow(table, rowIndex, row);
        }
    }else{
        createRow(table, rowIndex, row);    
    }
    openIcon.classList.add('');
    openIcon.classList.remove('');
}

function createRow(table, rowIndex, row){
    const newRow = table.insertRow(rowIndex+1);
    const rowData = row.getElementsByTagName("td");
    newRow.classList.add("shown");
    //insert and colspam cells
    const tdataIndex = newRow.insertCell(0);
    // tdataIndex.colSpan = 2;
    const tdataDetails = newRow.insertCell(1);
    //insert tags into table
    tdataDetails.colSpan = 8;
    tdataIndex.innerText = "";
    tdataDetails.innerHTML = `<p> Name: <strong>${rowData[1].innerText}</strong> </p>`;
    tdataDetails.innerHTML += `<p> Time requested: <strong>${rowData[4].innerText}</strong> </p>`;
    tdataDetails.innerHTML += `<p> Description: <strong>${rowData[3].innerText}</strong> </p>`;
    tdataDetails.innerHTML += `<p> Status: <strong>${rowData[6].innerText}</strong></p>`;
    

}
showSlide(1); 
