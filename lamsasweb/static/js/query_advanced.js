var tables = document.querySelector("#tables"),
    columns = document.querySelector("#columns"),
    orderBy = document.querySelector("#orderBy"),
    nullsLast = document.querySelector("#nullsLast"),
    limit = document.querySelector("#limit"),
    offset = document.querySelector("#offset"),
    distinct = document.querySelector("#distinct"),
    showQuery = document.querySelector("#showQuery"),
    whereCols = document.querySelector("#where_left"),
    whereOp = document.querySelector("#whereOperator"),
    whereExp = document.querySelector("#where_right");

initalizeForm();

function newOrderFields() {
  let orderByHeight = document.getElementById('orderBys').offsetHeight;
  makeOrderByField();
  makeNullsLastField();
}

function makeOrderByField() {
  let [newRow, newCol] = makeRowAndCol(['row'], ['col-md-12', 'mb-3']);

  let newOrderBy = document.createElement('select');
  newOrderBy.classList.add('form-select');
  newOrderBy.classList.add('form-select-lg');
  newOrderBy.disabled = true;
  prependEmptyOption(newOrderBy);

  newCol.appendChild(newOrderBy);
  document.getElementById('orderBys').appendChild(newRow);
}

function makeNullsLastField() {
  let newRowDiv = document.createElement('div');
  newRowDiv.classList.add('row');

  let newColDiv = document.createElement('div');
  newColDiv.classList.add('col-md-12');
  newColDiv.classList.add('mb-3');
  newColDiv.classList.add('mt-3');

  let newFormSwitchDiv = document.createElement('div');
  newFormSwitchDiv.classList.add('form-switch');
  newFormSwitchDiv.classList.add('mb-3');

  let newNullsLast = document.createElement('checkbox');
  newNullsLast.classList.add('form-check-input');

  newFormSwitchDiv.appendChild(newNullsLast);
  newColDiv.appendChild(newFormSwitchDiv);
  newRowDiv.appendChild(newColDiv);
  document.getElementById('orderBys').appendChild(newRowDiv);
}

function resetWhereOp() {
    whereOp.disabled = true;
    getSelectedOption(whereOp).selected = false;
    whereOp.querySelector('option').selected = true;
}

function addErrors() {
  for (let field in errors){
    window[field].classList.add("is-invalid");
  }
}

function resetAllElements() {
    resetElements([columns,
        orderBy,
        nullsLast,
        limit,
        offset,
        distinct,
        showQuery,
        whereCols,
        whereExp
    ]);
    resetWhereOp();
}

function initalizeForm() {
    resetAllElements();
    prependEmptyOption(tables);
    prependEmptyOption(whereOp);
    for (let key in all_columns) {
        appendOption(tables, key, key);
    }
    addErrors();
}

function tablesChange() {
    resetAllElements();
    if (!tables.querySelector("option").value) {
        tables.removeChild(tables.querySelector("option"));
    }
    let cols = all_columns[getSelectedOption(tables).value];
    for (let i in cols) {
        appendOption(columns, cols[i], cols[i]);
    }
    enableElements([columns]);
}

function columnsChange() {
    removeAllOptions(orderBy);
    removeAllOptions(whereCols);
    prependEmptyOption(orderBy);
    prependEmptyOption(whereCols);
    whereCols.required = false;
    whereOp.required = false;
    whereExp.required = false;
    let values = getSelectedValues(columns);
    for (let i in values) {
        appendOption(whereCols, values[i], values[i]);
        appendOption(orderBy, values[i]+", Asc.", values[i]+" ASC");
        appendOption(orderBy, values[i]+", Desc.", values[i]+" DESC");
    }
    if (columns.selectedIndex == -1){
        resetElements([orderBy, limit, offset, distinct, whereCols, whereExp, showQuery]);
    }else{
        enableElements([orderBy, limit, distinct, whereCols, showQuery]);
    }
}

function orderByChange() {
    if (orderBy.value) {
        enableElements([nullsLast]);
    } else {
        resetElements([nullsLast]);
    }
}

function limitChange() {
    if (limit.value) {
        enableElements([offset]);
    } else {
        resetElements([offset]);
    }
}

function offsetChange() {
    if (offset.value) {
        limit.toggleAttribute("required", true);
    } else {
        limit.toggleAttribute("required", false);
    }
}

function whereColsChange() {
     if (whereCols.value) {
        enableElements([whereOp, whereExp]);
        whereCols.required = true;
        whereOp.required = true;
        whereExp.required = true;
    } else {
        resetElements([whereExp]);
        resetWhereOp();
        whereCols.required = false;
        whereOp.required = false;
        whereExp.required = false;
    }
}
