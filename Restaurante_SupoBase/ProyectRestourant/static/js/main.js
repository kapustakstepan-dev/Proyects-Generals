document.addEventListener('DOMContentLoaded', () => {

    const logo = document.querySelector('.logo');
    logo.addEventListener('click', (e) => {
        e.preventDefault();
        logo.classList.add('neon-flash');
        setTimeout(() => {
            window.location.href = "/home";
        }, 500);
    });


    const btnLogin = document.getElementById('btn-login-tab');
    const btnReg = document.getElementById('btn-reg-tab');
    const formLogin = document.getElementById('form-login');
    const formReg = document.getElementById('form-reg');

    if(btnLogin) {
        btnLogin.addEventListener('click', () => {
            formLogin.classList.remove('hidden');
            formReg.classList.add('hidden');
            btnLogin.classList.add('active');
            btnReg.classList.remove('active');
        });

        btnReg.addEventListener('click', () => {
            formLogin.classList.add('hidden');
            formReg.classList.remove('hidden');
            btnReg.classList.add('active');
            btnLogin.classList.remove('active');
        });
    }
});

function sendInvoice() {
    alert("Invoice generated! A copy has been sent to your registered email (Placeholder).");
}