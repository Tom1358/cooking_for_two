function addIngredient(){
    console.log("Add button clicked")
}

function minusIngredient(){
    console.log("Minus button clicked")
}

document.getElementById("add-ingredient").addEventListener("click", addIngredient);

document.getElementById("minus-ingredient").addEventListener("click", minusIngredient);