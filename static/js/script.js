let addIngredientDiv = document.getElementById("add-ingredient-div");

function addIngredient(){
    console.log("Add button clicked")
    let newIngredient = `
        <div class="input-group form-group">

        <div class="input-group-prepend">
            <span class="input-group-text"><i class="fas fa-utensil-spoon"></i></span>
        </div>
        
        <input id="ingredients" name="ingredients" type="text" class="form-control validate" minlength="5"
            maxlength="35" placeholder="Ingredient ${1}" required>
        
        <div class="input-group-prepend">
            <span class="input-group-text"><a id="minus-ingredient"><i class="fas fa-minus"></i></a></span>
        </div>
        
        </div>
    `
    addIngredientDiv.innerHTML += newIngredient
}

function minusIngredient(){
    console.log("Minus button clicked")
    newIngredient.remove(this);
}

document.getElementById("add-ingredient").addEventListener("click", addIngredient);

document.getElementById("minus-ingredient").addEventListener("click", minusIngredient);
