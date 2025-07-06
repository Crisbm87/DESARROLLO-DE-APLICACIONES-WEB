document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const ageInput = document.getElementById('age');
    const submitButton = document.getElementById('submitButton');
    const resetButton = document.getElementById('resetButton');

    const nameError = document.getElementById('nameError');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');
    const confirmPasswordError = document.getElementById('confirmPasswordError');
    const ageError = document.getElementById('ageError');

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // La contraseña debe tener al menos 8 caracteres, al menos un número y un carácter especial
    const passwordRegex = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-zA-Z]).{8,}$/;

    const validateField = (input, errorElement, validationFn, errorMessage) => {
        if (validationFn(input.value)) {
            input.classList.remove('invalid');
            input.classList.add('valid');
            errorElement.textContent = '';
            return true;
        } else {
            input.classList.remove('valid');
            input.classList.add('invalid');
            errorElement.textContent = errorMessage;
            return false;
        }
    };

    const validateName = () => {
        return validateField(
            nameInput,
            nameError,
            (value) => value.length >= 3,
            'El nombre debe tener al menos 3 caracteres.'
        );
    };

    const validateEmail = () => {
        return validateField(
            emailInput,
            emailError,
            (value) => emailRegex.test(value),
            'El correo electrónico no tiene un formato válido.'
        );
    };

    const validatePassword = () => {
        return validateField(
            passwordInput,
            passwordError,
            (value) => passwordRegex.test(value),
            'La contraseña debe tener al menos 8 caracteres, un número y un carácter especial.'
        );
    };

    const validateConfirmPassword = () => {
        const passwordMatch = confirmPasswordInput.value === passwordInput.value;
        const passwordValid = passwordRegex.test(passwordInput.value); // Check if original password is valid

        if (passwordMatch && passwordValid) {
            confirmPasswordInput.classList.remove('invalid');
            confirmPasswordInput.classList.add('valid');
            confirmPasswordError.textContent = '';
            return true;
        } else {
            confirmPasswordInput.classList.remove('valid');
            confirmPasswordInput.classList.add('invalid');
            if (!passwordValid) {
                confirmPasswordError.textContent = 'Primero corrige la contraseña principal.';
            } else {
                confirmPasswordError.textContent = 'Las contraseñas no coinciden.';
            }
            return false;
        }
    };

    const validateAge = () => {
        return validateField(
            ageInput,
            ageError,
            (value) => parseInt(value) >= 18 && value !== '',
            'Debes tener al menos 18 años.'
        );
    };

    const validateForm = () => {
        const isNameValid = validateName();
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();
        const isConfirmPasswordValid = validateConfirmPassword();
        const isAgeValid = validateAge();

        submitButton.disabled = !(isNameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid && isAgeValid);
    };

    // Event listeners para validación en tiempo real
    nameInput.addEventListener('input', validateForm);
    emailInput.addEventListener('input', validateForm);
    passwordInput.addEventListener('input', validateForm);
    confirmPasswordInput.addEventListener('input', validateForm);
    ageInput.addEventListener('input', validateForm);

    // Event listener para el botón de reinicio
    resetButton.addEventListener('click', () => {
        form.reset();
        // Limpiar estilos y mensajes de error
        document.querySelectorAll('input').forEach(input => {
            input.classList.remove('valid', 'invalid');
        });
        document.querySelectorAll('.error-message').forEach(span => {
            span.textContent = '';
        });
        submitButton.disabled = true; // Deshabilitar el botón de envío
    });

    // Event listener para el envío del formulario
    form.addEventListener('submit', (event) => {
        event.preventDefault(); // Prevenir el envío por defecto del formulario

        if (!submitButton.disabled) {
            alert('¡Formulario enviado con éxito!');
            // Aquí podrías agregar lógica para enviar los datos a un servidor
            form.reset(); // Opcional: Reiniciar el formulario después del envío exitoso
            // Limpiar estilos y mensajes de error después de reiniciar
            document.querySelectorAll('input').forEach(input => {
                input.classList.remove('valid', 'invalid');
            });
            document.querySelectorAll('.error-message').forEach(span => {
                span.textContent = '';
            });
            submitButton.disabled = true;
        } else {
            alert('Por favor, corrige los errores del formulario antes de enviarlo.');
        }
    });

    // Validar el formulario al cargar la página para establecer el estado inicial del botón de envío
    validateForm();
});