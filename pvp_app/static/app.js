console.log('javascript is connected')

// event listener on reset button

const reset = document.querySelector('.reset');
reset.addEventListener('click', (event) => {
  console.log(event.target);
  const inputs = document.querySelectorAll('input');
  console.log(inputs);
  for (let index = 1; index < inputs.length; index++) {
    inputs[index].value = '';
    inputs[index].defaultValue = '';
  }
  inputs[1].focus();
})

// event listener on inputs
const body = document.querySelector('body');
// skip the csrf token hidden input
body.addEventListener('click', (event) => {
  console.log(event);
  if (event.target.localName == 'input') {
    event.target.select();
  }
})

// event listener to add new row of inputs
const add_button = document.querySelector('#add');

add_button.addEventListener('click', (event) => {
  let input_rows = document.querySelector('.IVInputsContainer');
  const new_row = document.createElement('div');
  let IV_row = document.querySelector('.IVs');
  new_row.innerHTML = IV_row.innerHTML;

  let elems = new_row.getElementsByTagName('input');
  let atk_input = undefined;
  
  for (let i = 0; i < elems.length; i++) {
    if (elems[i].id == 'attack') {
      atk_input = elems[i]
    }

    console.log(elems[i])
    // elems[i].value = '';
    // elems[i].defaultValue = '';
    elems[i].removeAttribute('value');
  }

  new_row.classList.add('IVs');
  input_rows.appendChild(new_row);
  atk_input.focus();
})

// event listener to add new row on tab press
let input_rows = document.querySelector('.IVInputsContainer');

input_rows.addEventListener('keydown', (event) => {
  console.log(event)
  // don't perform action if shift + tab pressed
  // make new row if tab pressed, input is stamina field, and it's the last row of inputs in the form
  if (event.key == 'Tab' && event.shiftKey == false && event.target.id == 'stamina' && event.target.parentElement.nextElementSibling == null) {
    console.log('pressed Tab')
    let input_rows = document.querySelector('.IVInputsContainer');
    const new_row = document.createElement('div');
    let IV_row = document.querySelector('.IVs');
    new_row.innerHTML = IV_row.innerHTML;

    let elems = new_row.getElementsByTagName('input');

    for (let i = 0; i < elems.length; i++) {
      console.log(elems[i])
      elems[i].removeAttribute('value');
    }


    new_row.classList.add('IVs');
    input_rows.appendChild(new_row);
  }
})