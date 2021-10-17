let addIngredientDiv = document.getElementById("add-ingredient-div");

// document.getElementById("minus-ingredient").addEventListener('click', minusIngredientFunction);




function addIngredient(){
    console.log("Add button clicked")
    let newIngredient = `
        <div class="input-group form-group extra-item">

        <div class="input-group-prepend">
            <span class="input-group-text"><i class="fas fa-utensil-spoon"></i></span>
        </div>
        
        <input id="ingredients" name="ingredients" type="text" class="form-control validate" minlength="5"
            maxlength="35" placeholder="" required>
        
        <div class="input-group-prepend">
            <span class="input-group-text"><a id="minus-ingredient"><i class="fas fa-minus"></i></a></span>
        </div>
        
        </div>
    `
    addIngredientDiv.innerHTML += newIngredient
}

function minusIngredientFunction(){
    console.log("Minus button clicked")
    // let deleteItem = document.getElementById("extra-item")
    // this.remove(deleteItem);
}

// document.getElementById("add-ingredient").addEventListener("click", addIngredient);


