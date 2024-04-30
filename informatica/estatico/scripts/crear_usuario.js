$(document).ready(function () {

    $("#btnCrearUsuario").click(function (event) {
        event.preventDefault();
        if (validarFormulario($("#frmCrearUsuario")).valido) {
            $.ajax({
                type: "POST",
                url: "/informatica/gestion-usuarios/crear-usuario",
                data: $("#frmCrearUsuario, #idPersona").serialize(),
                success: function (respuesta) {
                    if (respuesta.noidPersona) {
                        abrirModal("Asignar persona", "Seleccione el empleado.", "")
                    }
                    if (respuesta.creado) {
                        abrirModal("Usuario creado", "El usuario " + respuesta.usuario + " ha sido registrado correctamente.", "recargar")
                    }
                    if (respuesta.modificado) {
                        console.log("MODIFICADO")
                        abrirModal("Usuario modificado", "El usuario " + respuesta.usuario + " ha sido modificado.", "recargar")
                    }
                    if (respuesta.existente) {
                        console.log("existente")
                        abrirModal("Usuario existente", "El usuario " + respuesta.usuario + " ya existe.", "")
                    }

                }
            });
        }
    });
});
