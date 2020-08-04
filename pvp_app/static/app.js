console.log('javascript is connected')

// event listener on reset button

// const reset = document.querySelector('.reset');
// reset.addEventListener('click', (event) => {
//   console.log(event.target);
//   const inputs = document.querySelectorAll('input');
//   console.log(inputs);
//   for (let index = 1; index < inputs.length; index++) {
//     inputs[index].value = '';
//     inputs[index].defaultValue = '';
//   }
//   inputs[1].focus();
// })

// event listener to highlight input text on click
const body = document.querySelector('body');
// skip the csrf token hidden input
body.addEventListener('click', (event) => {
  console.log(event);
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

  let elems = new_row.getElementsByTagName('input');
  let cp_input = undefined;
  
  for (let i = 0; i < elems.length; i++) {
    if (elems[i].id == 'cp') {
      cp_input = elems[i]
    }

    // remove values from previous inputs
    elems[i].removeAttribute('value');
    // remove invalid flag that would turn background pink
    elems[i].classList.remove('invalid');
  }

  new_row.classList.add('IVs');
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
  console.log(event)
  // don't perform action if shift + tab pressed
  // make new row if tab pressed, input is stamina field, and it's the last row of inputs in the form
  if (event.key == 'Tab' && event.shiftKey == false && event.target.id == 'stamina' && event.target.parentElement.nextElementSibling == null) {
    console.log('pressed Tab');
    copyRows(event);
  }
})


// event listener to validate inputs
input_rows.addEventListener('focusout', (event) => {
  // validate CP inputs
  if (event.target.id == 'cp') {
    if (event.target.value < 10) {
      console.log('invalid CP')
      // event.target.focus()
      // event.target.select()
      event.target.classList.add('invalid')
    }
    if (event.target.value >= 10) {
      console.log('should not be pink')
      event.target.classList.remove('invalid')
    }
    checkForInvalidInputs();
  }
  // validate IV inputs
  console.log(event)
  console.log('left input')
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