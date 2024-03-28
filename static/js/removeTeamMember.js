var memberData = document.getElementsByClassName("memberData")
const BASE_PATH = window.location.origin
function dataMember(name, email, teamID) {
    memberData[0].innerHTML=`Eliminar al usuario <strong>${name}</strong> - <strong>${email}</strong> de tu equipo.`
    var deleteMemberURL = document.getElementsByClassName("deleteMemberURL")[0]
    deleteMemberURL.addEventListener("click", function(event) {
        event.preventDefault(); // Prevenir la acción predeterminada del enlace
        
        // Crear un formulario dinámicamente
        var formulario = document.createElement('form');
        formulario.innerHTML = "{{csrf_token}}"
        formulario.method = 'POST'; // Método POST
        formulario.action = `${BASE_PATH}/teams/edit/remove/${teamID}/`; // URL de destino
        
        // Agregar campo de token CSRF al formulario
        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        var tokenCSRF = document.createElement('input');
        tokenCSRF.type = 'hidden';
        tokenCSRF.name = 'csrfmiddlewaretoken';
        tokenCSRF.value = csrfToken;
        formulario.appendChild(tokenCSRF);

        // Agregar campos al formulario
        var campo1 = document.createElement('input');
        campo1.type = 'hidden'; // Campo oculto
        campo1.name = 'username'; // Nombre del campo
        campo1.value = `${name}`; // Valor del campo
        formulario.appendChild(campo1); // Agregar campo al formulario
        
        var campo2 = document.createElement('input');
        campo2.type = 'hidden';
        campo2.name = 'email';
        campo2.value = `${email}`;
        formulario.appendChild(campo2);
        
        // Agregar formulario al cuerpo del documento
        document.body.appendChild(formulario);
        
        // Enviar formulario
        formulario.submit();
    });
}

