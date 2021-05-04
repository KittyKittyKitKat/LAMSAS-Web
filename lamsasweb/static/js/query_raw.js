var raw_query = document.querySelector("#raw_query");

initalizeForm();

function resetAllElements() {
    resetElements([raw_query], disable = false);
}

function addErrors() {
  for (var field in errors){
    window[field].classList.add("is-invalid");
  }
}

function initalizeForm() {
    resetAllElements();
    addErrors();
}
