$(document).ready(function() {
    
    $("#btnCrearUsuario").click(function (event) {
        event.preventDefault();
        if (validarFormulario($("#frmCrearUsuario")).valido) {
            $.ajax({
                type: "POST",
                url: "/informatica/crear-usuario",
                data: $("#frmCrearUsuario").serialize(),
                success: function (respuesta) {
                 if (respuesta.creado){
                     console.log("CREADO")
                 }
                if (respuesta.modificado){
                    console.log("MODIFICADO")
                }
                  
                }
            });
        }
    });
});
