const form = document.querySelector('.form-singup')
const username = document.querySelector('#username')
const password = document.querySelector('#password1')
const password2 = document.querySelector('#password2')
let passwRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/

username.addEventListener('input', e => {
    if (username.value.length < 6) {
      username.style.border = '1px solid red';
    } else {
      username.style.border = '1px solid green';
    }
  })

password.addEventListener('input', e => {
    if (password.value.length < 6 || !passwRegex.test(password.value) && password2.value != password.value) {
      password.style.border = '1px solid red';
    } else {
      password.style.border = '1px solid green';
    }

    if (password2.value !== '' && password2.value !== password1.value) {
        password2.style.border = '1px solid red';
      } else if (password2.value === password.value && password2.value !== '') {
        password2.style.border = '1px solid green';
      }
})

password2.addEventListener('input', e => {
    if (password2.value.length < 6 || !passwRegex.test(password2.value)) {
        password2.style.border = '1px solid red';
      } else if (password2.value === password.value && password2.value !== '') {
        password2.style.border = '1px solid green';
      } else {
        password2.style.border = '1px solid red';
      }
})



form.addEventListener("submit", e => {
    e.preventDefault();
    let entrar = false;
    if (username.value.length < 6) {
      entrar = true;
    }
  
    if (password.value.length < 6 || !passwRegex.test(password.value)) {
      entrar = true;
    }
  
    if (!entrar) {
      form.submit();
    }
})