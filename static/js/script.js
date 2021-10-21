// Empty div to store template literal in for new input
let addIngredientDiv = document.getElementById("add-ingredient-div");

// '+' Button on input field for ingredient
let add_ingredient = document.getElementById("add-ingredient")

// counter starts at two as user will be adding second ingredient
let ingredient_count = 2;

// function if '+' button is pressed
function addIngredient(){
    console.log("Add button clicked")
    let newIngredient = `
        <div class="input-group form-group extra-item" id="extra-item">

        <div class="input-group-prepend">
            <span class="input-group-text"><i class="fas fa-utensil-spoon"></i></span>
        </div>
        
        <input id="ingredients" name="ingredients" type="text" class="form-control validate" minlength="5"
            placeholder="" required>
        
        <div class="input-group-prepend">
            <span class="input-group-text"><a class="minus-ingredient" onclick="minusIngredientFunction"><i class="fas fa-minus"></i></a></span>
        </div>
        
        </div>
    `
    let extraItem = document.createElement("div")

    // Adds above template literal into new empty div
    extraItem.innerHTML += newIngredient
    addIngredientDiv.appendChild(extraItem)

    // Sets id of new input as the ingredient number (i.e. 3rd ingredient is ingredient_count_3)
    extraItem.setAttribute("id", `ingredient_count_${ingredient_count}`)

    // for test purposes
    console.log(extraItem)
    console.log(ingredient_count)

    // After each ingredient added, counter increases ready for next ingredient
    ingredient_count ++;

}

// For other HTML pages on site, nothing happens if can't find add_ingredient (the '+' sign)
if (add_ingredient != null) {
    add_ingredient.addEventListener("click", addIngredient);
}

// document.getElementById(`ingredient_count_${ingredient_count}`).addEventListener("click", remove());

// console.log("Minus button clicked")
// })
