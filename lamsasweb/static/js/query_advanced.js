var tables = document.querySelector("#tables"),
    columns = document.querySelector("#columns"),
    order_by = document.querySelector("#order_by"),
    nulls_last = document.querySelector("#nulls_last"),
    limit = document.querySelector("#limit"),
    offset = document.querySelector("#offset"),
    distinct = document.querySelector("#distinct"),
    show_query = document.querySelector("#show_query"),
    where_cols = document.querySelector("#where_left"),
    where_op = document.querySelector("#where_operator"),
    where_exp = document.querySelector("#where_right");

initalizeForm();

function newOrderFields() {
  let order_by_height = document.getElementById('order_bys').offsetHeight;
  makeOrderByField();
  makeNullsLastField();
}

function makeOrderByField() {
  let [new_row, new_col] = makeRowAndCol(['row'], ['col-md-12', 'mb-3']);

  let new_order_by = document.createElement('select');
  new_order_by.classList.add('form-select');
  new_order_by.classList.add('form-select-lg');
  new_order_by.disabled = true;
  prependEmptyOption(new_order_by);

  new_col.appendChild(new_order_by);
  document.getElementById('order_bys').appendChild(new_row);
}

function makeNullsLastField() {
  let new_row_div = document.createElement('div');
  new_row_div.classList.add('row');

  let new_col_div = document.createElement('div');
  new_col_div.classList.add('col-md-12');
  new_col_div.classList.add('mb-3');
  new_col_div.classList.add('mt-3');

  let new_form_switch_div = document.createElement('div');
  new_form_switch_div.classList.add('form-switch');
  new_form_switch_div.classList.add('mb-3');

  let new_nulls_last = document.createElement('checkbox');
  new_nulls_last.classList.add('form-check-input');

  new_form_switch_div.appendChild(new_nulls_last);
  new_col_div.appendChild(new_form_switch_div);
  new_row_div.appendChild(new_col_div);
  document.getElementById('order_bys').appendChild(new_row_div);
}

function resetWhereOp() {
    where_op.disabled = true;
    getSelectedOption(where_op).selected = false;
    where_op.querySelector('option').selected = true;
}

function addErrors() {
  for (let field in errors){
    window[field].classList.add("is-invalid");
  }
}

function resetAllElements() {
    resetElements([columns,
        order_by,
        nulls_last,
        limit,
        offset,
        distinct,
        show_query,
        where_cols,
        where_exp
    ]);
    resetWhereOp();
}

function initalizeForm() {
    resetAllElements();
    prependEmptyOption(tables);
    prependEmptyOption(where_op);
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
    removeAllOptions(order_by);
    removeAllOptions(where_cols);
    prependEmptyOption(order_by);
    prependEmptyOption(where_cols);
    where_cols.required = false;
    where_op.required = false;
    where_exp.required = false;
    let values = getSelectedValues(columns);
    for (let i in values) {
        appendOption(where_cols, values[i], values[i]);
        appendOption(order_by, values[i]+", Asc.", values[i]+" ASC");
        appendOption(order_by, values[i]+", Desc.", values[i]+" DESC");
    }
    if (columns.selectedIndex == -1){
        resetElements([order_by, limit, offset, distinct, where_cols, where_exp, show_query]);
    }else{
        enableElements([order_by, limit, distinct, where_cols, show_query]);
    }
}

function order_byChange() {
    if (order_by.value) {
        enableElements([nulls_last]);
    } else {
        resetElements([nulls_last]);
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

function where_colsChange() {
     if (where_cols.value) {
        enableElements([where_op, where_exp]);
        where_cols.required = true;
        where_op.required = true;
        where_exp.required = true;
    } else {
        resetElements([where_exp]);
        resetWhereOp();
        where_cols.required = false;
        where_op.required = false;
        where_exp.required = false;
    }
}
