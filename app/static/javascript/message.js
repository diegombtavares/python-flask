function mostrarSenha() {
    var senhaInput = document.getElementById("senha");
    var iconeOlho = document.querySelector(".input-icon-right i");

    if (senhaInput.type === "password") {
        senhaInput.type = "text";
        iconeOlho.classList.remove("fa-eye");
        iconeOlho.classList.add("fa-eye-slash");
    } else {
        senhaInput.type = "password";
        iconeOlho.classList.remove("fa-eye-slash");
        iconeOlho.classList.add("fa-eye");
    }
}

document.addEventListener('DOMContentLoaded', function() {
    var messages = document.getElementById('messages');

    if (messages) {
        // Adicione a classe para a transição de opacidade
        messages.classList.add('message-transition');

        setTimeout(function() {
            messages.style.opacity = '0';
            setTimeout(function() {
                messages.remove();
            }, 500);
        }, 5000);
    }
});