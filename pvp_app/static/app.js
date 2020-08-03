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