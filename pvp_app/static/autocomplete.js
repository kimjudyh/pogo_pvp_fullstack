// javascript to autocomplete Pokemon and Evolution Pokemon fields
console.log('autocomplete js connected')

// function to get CSRF cookie from token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

let pokemon = { options: [] };
let evoPokemon = { options: [] };
// make GET request to backend
function findMatches(event) {
    let searchString = event.target.value;
    let matches_array = [];

    // only need to search once, then the datalist will contain all relevant results and can be filtered without querying the database
    if (searchString.length == 1) {
        // fetch from API endpoint 'search/<str:pokemon>'
        fetch(
            `/search/${searchString}`,
            {
                method: 'GET',
                headers: {
                Accept: "application/json",
                "X-CSRFToken": csrftoken,
                }
            }
        )
        .then((res) => res.json())
        .then((data) => {
            // take JSON and convert results list into datalist options
            // console.log(data.results);
            matches_array = data.results;
            let pokemonDataList = document.querySelector('#auto-pokemon');
            let evoPokemonDataList = document.querySelector('#auto-evo-pokemon')
            let pokemonInput = document.querySelector('#pokemon');

            // delete old options
            pokemonDataList.innerHTML = '';
            evoPokemonDataList.innerHTML = '';
            // create option elements, append to datalist
            matches_array.forEach((match, index) => {
                let option = document.createElement('option');
                option.value = match;
                if (index == 0) {
                    // set first option to be selected by default
                    option.selected = true;
                }
                if (event.target.id == 'pokemon') {
                    pokemonDataList.appendChild(option);
                }
                else if (event.target.id == 'evo-pokemon') {
                    evoPokemonDataList.appendChild(option);
                }
            })
        })
        .catch((err) => console.log(err))
    }
}

function getEvolutions(event) {
    let searchString = event.target.value;
    let matches_array = [];
    // fetch from API endpoint 'evolutions/<str:pokemon>'
    fetch(
        `/evolutions/${searchString}`,
        {
            method: 'GET',
            headers: {
            Accept: "application/json",
            "X-CSRFToken": csrftoken,
            }
        }
    )
    .then((res) => res.json())
    .then((data) => {
        matches_array = data.results;
        // console.log(matches_array)
        let evoPokemonDataList = document.querySelector('#auto-evo-pokemon')
        let evoPokemonInput = document.querySelector('#evo-pokemon');
        evoPokemonDataList.innerHTML = '';
        matches_array.forEach((match, index) => {
            let option = document.createElement('option');
            option.value = match;
            // if (index == 0) {
            //     // set first option to be selected by default
            //     option.selected = true;
            // }
            evoPokemonDataList.appendChild(option);
            evoPokemonInput.value = '';
        })
    })
    .catch((err) => console.log(err))

}

let pokemonInput = document.querySelector('#pokemon');
let evoPokemonInput = document.querySelector('#evo-pokemon');
// add event listener to pokemon input field
pokemonInput.addEventListener('keypress', findMatches);
// add event listener to completion inside pokemon input field
pokemonInput.addEventListener('focusout', getEvolutions);
// add event listener to evo pokemon input field
// evoPokemonInput.addEventListener('keyup', findMatches);

// event listener to check for invalid Pokemon or evolution pokemon entries
// pokemonInput.addEventListener('keyup', checkForInvalidInputs);
// evoPokemonInput.addEventListener('focus', checkForInvalidInputs);

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

