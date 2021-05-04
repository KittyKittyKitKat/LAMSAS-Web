var tables = document.querySelector("#tables"),
    columns = document.querySelector("#columns"),
    orderBy = document.querySelector("#orderBy"),
    distinct = document.querySelector("#distinct"),
    limit = document.querySelector("#limit");

initalizeForm();

function resetAllElements() {
    resetElements([columns,
        orderBy,
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
    removeAllOptions(orderBy);
    prependEmptyOption(orderBy);
    var values = getSelectedValues(columns);
    for (var i in values) {
        appendOption(orderBy, values[i]+", Asc.", values[i]+" ASC");
        appendOption(orderBy,  values[i]+", Desc.", values[i]+" DESC");
    }
    if (columns.selectedIndex == -1){
        resetElements([orderBy, limit, distinct]);
    }else{
        enableElements([orderBy, limit, distinct]);
    }
}

function orderByChange(){}
function limitChange(){}
