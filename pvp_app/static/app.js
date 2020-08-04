console.log('javascript is connected')


// event listener to highlight input text on click
const body = document.querySelector('body');
// skip the csrf token hidden input
body.addEventListener('click', (event) => {
  if (event.target.localName == 'input') {
    event.target.select();
  }
})


// function to copy input html markup and reset values, styling
function copyRows(event) {
  let input_rows = document.querySelector('.IVInputsContainer');
  const new_row = document.createElement('div');
  let IV_row = document.querySelector('.IVs');
  new_row.innerHTML = IV_row.innerHTML;

  // remove error message div
  let error_elems = new_row.getElementsByClassName('invalidCombo') 
    for (let i = 0; i < error_elems.length; i++) {
      error_elems[i].remove();
    }
  

  let delete_elems = new_row.getElementsByClassName('delete');
  for (let i = 0; i < delete_elems.length; i++) {
    // enable deletion of new row
    delete_elems[i].removeAttribute('disabled');
  }

  let input_elems = new_row.getElementsByTagName('input');
  let cp_input = undefined;
  
  for (let i = 0; i < input_elems.length; i++) {
    if (input_elems[i].id == 'cp') {
      cp_input = input_elems[i]
    }

    // remove values from previous inputs
    input_elems[i].removeAttribute('value');
    // remove invalid flag that would turn background pink
    input_elems[i].classList.remove('invalid');
  }

  new_row.classList.add('IVs');
  new_row.classList.add('form-inline');
  input_rows.appendChild(new_row);
  if (event.type == 'click') {
    cp_input.focus();

  }
}

// event listener to add new row of inputs
const add_button = document.querySelector('#add');

add_button.addEventListener('click', copyRows) 

let input_rows = document.querySelector('.IVInputsContainer');

// event listener to add new row on tab press
input_rows.addEventListener('keydown', (event) => {
  // don't perform action if shift + tab pressed
  // make new row if tab pressed, input is stamina field, and it's the last row of inputs in the form
  if (event.key == 'Tab' && event.shiftKey == false && event.target.id == 'stamina' && event.target.parentElement.nextElementSibling == null && event.target.value != '') {
    copyRows(event);
  }
})


// event listener to validate inputs
input_rows.addEventListener('focusout', (event) => {
  // validate CP inputs
  if (event.target.id == 'cp') {
    if (event.target.value < 10) {
      // console.log('invalid CP')
      // event.target.focus()
      // event.target.select()
      event.target.classList.add('invalid')
    }
    if (event.target.value >= 10) {
      event.target.classList.remove('invalid')
    }
    checkForInvalidInputs();
  }
  // validate IV inputs
  // console.log('left input')
  if (event.target.id == 'attack' || event.target.id == 'defense' || event.target.id == 'stamina') {
    if (event.target.value > 15 || event.target.value < 0 || event.target.value == '') {
      console.log('invalid')
      event.target.classList.add('invalid')
      // event.target.focus()
      // event.target.select()
    }
    if (event.target.value <= 15 && event.target.value >= 0 && event.target.value != '') {
      event.target.classList.remove('invalid')
    }
  }
  checkForInvalidInputs();

})

// don't allow form submission if there are any invalid inputs
function checkForInvalidInputs() {
  let invalid_inputs = document.querySelectorAll('.invalid');
  let analyze_button = document.querySelector('.analyze');
  if (invalid_inputs.length > 0) {
    analyze_button.classList.add('disabled');
    analyze_button.setAttribute('disabled', true);
  }
  else {
    analyze_button.classList.remove('disabled');
    analyze_button.removeAttribute('disabled');
  }

}

// delete row using button
// let delete_button = document.querySelector('.delete');
input_rows.addEventListener('click', (event) => {
  if (event.target.classList.contains('delete')) {
    let row_to_delete = event.target.parentElement;
    row_to_delete.remove();
    checkForInvalidInputs();
    // remove any Wrong CP & IV combo messages
  }

})