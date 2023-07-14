
const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const container = document.getElementById("container");

signUpButton.addEventListener('click', signInButtonClick);
signInButton.addEventListener('click', signUpButtonClick);

function signInButtonClick() {
    container.classList.add('right-panel-active');
    return fetch('/home')
}

function signUpButtonClick() {
    container.classList.remove('right-panel-active');;
}