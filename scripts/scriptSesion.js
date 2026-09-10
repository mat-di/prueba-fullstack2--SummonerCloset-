function validarCorreo(event){
    if(event.key == 'Enter'){
        
        const email = document.getElementById('email').value.trim();
        const confirmEmail = document.getElementById('confirmEmail').value.trim();

        if(email == '' || confirmEmail == ''){
            alert('Por favor, ingrese su correo electrónico');
            return;
        }
        else if(email != confirmEmail){
            alert('Los correos electrónicos no coinciden');
            return;
        }
    }
}