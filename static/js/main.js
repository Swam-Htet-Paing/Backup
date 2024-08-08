const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

const showHiddenPass = (passId, eyeId) => {
    const input = document.getElementById(passId);
    const iconEye = document.getElementById(eyeId);

    iconEye.addEventListener('click', () => {
        if (input.type === 'password') {
            input.type = 'text';
            iconEye.classList.add('fa-eye');
            iconEye.classList.remove('fa-eye-slash');
        } else {
            input.type = 'password';
            iconEye.classList.remove('fa-eye');
            iconEye.classList.add('fa-eye-slash');
        }
    });
}

showHiddenPass('login-pass', 'login-eye');
showHiddenPass('signup-pass', 'signup-eye');
