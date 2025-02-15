const form = document.querySelector("form")
fileInput = document.querySelector(".file-input")

form.addEventListener("click", ()=>{
    fileInput.click();
})

let file = fileInput.files[0];  // Get the selected file

// function uploadFile(name){
// //     let x = new XMLHttpRequest();
// //     x.open
// // }


console.log(file)
