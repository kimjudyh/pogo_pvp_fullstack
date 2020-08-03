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
  new_row.classList.add('IVs');
  input_rows.appendChild(new_row);
})

// event listener to add new row on tab press
let input_rows = document.querySelector('.IVInputsContainer');

input_rows.addEventListener('keydown', (event) => {
  console.log(event)
  if (event.key == 'Tab' && event.target.id == 'stamina') {
    console.log('pressed Tab')
    let input_rows = document.querySelector('.IVInputsContainer');
    const new_row = document.createElement('div');
    let IV_row = document.querySelector('.IVs');
    new_row.innerHTML = IV_row.innerHTML;
    new_row.classList.add('IVs');
    input_rows.appendChild(new_row);
  }
})