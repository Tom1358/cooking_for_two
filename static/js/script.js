let addIngredientDiv = document.getElementById("add-ingredient-div");

// function if add button is pressed
function addIngredient(){
    console.log("Add button clicked")
    let newIngredient = `
        <div class="input-group form-group extra-item">

        <div class="input-group-prepend">
            <span class="input-group-text"><i class="fas fa-utensil-spoon"></i></span>
        </div>
        
        <input id="ingredients" name="ingredients[]" type="text" class="form-control validate" minlength="5"
            placeholder="" required>
        
        <div class="input-group-prepend">
            <span class="input-group-text"><a class="minus-ingredient"><i class="fas fa-minus"></i></a></span>
        </div>
        
        </div>
    `
    let extraItem = document.createElement("div")
    extraItem.innerHTML += newIngredient
    addIngredientDiv.appendChild(extraItem)

    
}

// function if minus button pressed
function minusIngredientFunction(){
    console.log("minus button clicked")
}

// document.getElementById("add-ingredient").addEventListener("click", addIngredient);

// document.getElementsByClassName("minus-ingredient").addEventListener("click", minusIngredientFunction);

// document.addEventListener('click', function() {
// let minusIngredient = document.getElementsByClassName("minus-ingredient")

// console.log("Minus button clicked")
// })
