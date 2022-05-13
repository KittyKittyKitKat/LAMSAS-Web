var tiptextMap = {
    'tables': 'Select a table of data to draw from.',
    'columns': 'Select a column to order the data by.',
    'order_by': 'Select one or more columns of data (Hint: Hold Ctrl+Click to select multiple values).',
    'nulls_last': 'Put results with no data at the end of the ordering.',
    'limit': 'Set how many results to return.',
    'offset': 'Shift the offset of the data returned.',
    'distinct': 'Only return only unique results.',
    'show_query': 'Return the query in SQLite syntax.',
    'where_operator': 'Set a sorting condition for the data based on a column\'s relation to a value.',
    'raw_query': 'Enter a query in SQLite syntax.'
}

getSelectedOption = (selectElement) => selectElement.options[selectElement.selectedIndex];

function prependEmptyOption(selectElement) {
    var emptyOption = document.createElement("option");
    emptyOption.value = "";
    emptyOption.innerHTML = "";
    emptyOption.selected = true;
    selectElement.insertBefore(emptyOption, selectElement.firstChild);
}

function removeAllOptions(selectElement) {
    while (selectElement.options.length) {
        selectElement.remove(0);
    }
}

function appendOption(selectElement, text, value) {
    var opt = document.createElement("option");
    opt.innerHTML = text;
    opt.value = value;
    selectElement.appendChild(opt);
}

function getSelectedValues(selectElement) {
    var result = [];
    var options = selectElement && selectElement.options;
    var opt;
    for (var i=0; i<options.length; i++) {
        opt = options[i];
        if (opt.selected) {
          result.push(opt.value);
        }
    }
    return result;
}

function resetElements(elemsList, disable = true) {
    for (var i=0; i<elemsList.length; i++) {
        var elem = elemsList[i];
        if (elem !== null){}
          if (disable == true){
            elem.disabled = true;
          }
          if (elem.type.includes('text')) {
              elem.value = '';
          }
          if (elem.type == 'checkbox') {
              elem.checked = false;
          }
          if (elem.type.includes('select')) {
              removeAllOptions(elem);
        }
    }
}

function enableElements(elemsList) {
    for (var i=0; i<elemsList.length; i++) {
        elemsList[i].disabled = false;
    }
}

function registerTooltips() {
    for (var labelElem in tiptextMap) {
        currElemLabel = document.querySelector(`[for='${labelElem}']`);
        if (currElemLabel != null) {
            currElemLabel.setAttribute('data-bs-toggle', 'tooltip');
            currElemLabel.setAttribute('data-bs-placement', 'right');
            currElemLabel.setAttribute('title', tiptextMap[labelElem]);
        }
    }
}

function makeRowAndCol(rowClasses, colClasses) {
    var row = document.createElement('div');
    var col = document.createElement('div');
    for (var i = 0; i<rowClasses.length; i++){
      row.classList.add(rowClasses[i]);
    }
    for (var i = 0; i<colClasses.length; i++){
      col.classList.add(colClasses[i]);
    }
    row.appendChild(col);
    return [row, col];
}

registerTooltips();
