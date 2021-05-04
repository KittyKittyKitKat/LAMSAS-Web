var tables = document.querySelector("#tables"),
    columns = document.querySelector("#columns"),
    order_by = document.querySelector("#order_by"),
    distinct = document.querySelector("#distinct"),
    limit = document.querySelector("#limit");

initalizeForm();

function resetAllElements() {
    resetElements([columns,
        order_by,
        limit,
        distinct,
    ]);
}

function addErrors() {
  for (var field in errors){
    window[field].classList.add("is-invalid");
  }
}

function initalizeForm() {
    resetAllElements();
    prependEmptyOption(tables);
    for (var key in all_columns) {
        appendOption(tables, key, key);
    }
    addErrors();
}

function tablesChange() {
    resetAllElements();
    if (!tables.querySelector("option").value) {
        tables.removeChild(tables.querySelector("option"));
    }
    var cols = all_columns[getSelectedOption(tables).value];
    for (var i in cols) {
        appendOption(columns, cols[i], cols[i]);
    }
    enableElements([columns]);
}

function columnsChange() {
    removeAllOptions(order_by);
    prependEmptyOption(order_by);
    var values = getSelectedValues(columns);
    for (var i in values) {
        appendOption(order_by, values[i]+", Asc.", values[i]+" ASC");
        appendOption(order_by,  values[i]+", Desc.", values[i]+" DESC");
    }
    if (columns.selectedIndex == -1){
        resetElements([order_by, limit, distinct]);
    }else{
        enableElements([order_by, limit, distinct]);
    }
}

function order_byChange(){}
function limitChange(){}
