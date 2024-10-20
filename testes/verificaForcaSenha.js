let passwordVisible = false;

function togglePasswordVisibility(campo, icone) {
    const passwordInput = document.getElementById(campo);
    const passwordIcon = document.getElementById(icone);

    // Apenas alternar a visibilidade se houver texto no campo
    if (passwordInput.value.length > 0) {
        passwordVisible = !passwordVisible;
        passwordInput.type = passwordVisible ? 'text' : 'password';
    }
}

function togglePasswordIcon(password, iconId) {
    const passwordIcon = document.getElementById(iconId);

    if (password.length > 0) {
        passwordIcon.classList.remove('bi-lock');
        passwordIcon.classList.add('bi-eye');
    } else {
        passwordIcon.classList.remove('bi-eye');
        passwordIcon.classList.add('bi-lock');
    }
}

function toggleConfirmPasswordIcon(password) {
    const passwordIcon = document.getElementById('confirmPasswordIcon');

    if (password.length > 0) {
        passwordIcon.classList.remove('bi-check-circle');
        passwordIcon.classList.add('bi-eye');
    } else {
        passwordIcon.classList.remove('bi-eye');
        passwordIcon.classList.add('bi-check-circle');
    }
}

function changeCursor(icon, cursorType) {
    const passwordInput = document.getElementById('senha');
    if (passwordInput.value.length > 0) {
        icon.style.cursor = cursorType;
    } else {
        icon.style.cursor = 'default';
    }
}

// Função para manter o comportamento original dos campos
function clearValue(input, defaultValue) {
    if (input.value === defaultValue || input.value === '') {
        input.value = ''; // Limpa o valor do campo
    }
}

function restoreValue(input, defaultValue) {
    if (input.value === '') {
        input.value = defaultValue; // Restaura o valor padrão se o campo estiver vazio
    }
}



function checkPasswordStrength(password) {
    let strengthText = '';
    let transitions = 0;
    let lastType = '';

    function getCharType(char) {
        if (/[A-Z]/.test(char)) return 'upper';
        if (/[a-z]/.test(char)) return 'lower';
        if (/\d/.test(char)) return 'number';
        if (/[!@#$%^&*(),.?":{}|<>]/.test(char)) return 'special';
        return 'other';
    }

    for (let i = 0; i < password.length; i++) {
        const currentType = getCharType(password[i]);
        if (currentType !== lastType && currentType !== 'other') {
            transitions++;
            lastType = currentType;
        }
    }

    if (transitions < 2) {
        strengthText = 'Fraca';
        document.getElementById('senha-forca').className = 'senha-forca fraca';
    } else if (transitions >= 2 && transitions <= 5) {
        strengthText = 'Média';
        document.getElementById('senha-forca').className = 'senha-forca media';
    } else {
        strengthText = 'Forte';
        document.getElementById('senha-forca').className = 'senha-forca forte';
    }

    // Atualizar o texto na página e esconder a força se a senha estiver vazia
    document.getElementById('senha-forca').textContent = strengthText;

    if (password.length === 0) {
        document.getElementById('senha-forca').textContent = ''; // Oculta o texto se o campo estiver vazio
        passwordIcon.classList.remove('bi-eye'); // Volta para o ícone de lock
        passwordIcon.classList.add('bi-lock');
    }
}
