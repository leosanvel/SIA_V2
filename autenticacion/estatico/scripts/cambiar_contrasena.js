$gmx(document).ready(function () {
    $("#frmContrasenas").submit(function (event) {
        event.preventDefault();
        if (validarFormulario($("#frmContrasenas")).valido) {
            $.ajax({
                type: "POST",
                url: "/autenticacion/cambiar-contrasena",
                data: $("#frmContrasenas").serialize(),
                success: function (data) {
                    if (data.ContrasenaActual) {
                        if (data.NuevasContrasenasCoinciden) {
                            if (data.CambioContrasena) {
                                abrirModal("Contraseña modificada", "La contraseña ha sido cambiada correctamente.", "inicio");
                            }
                        } else {
                            abrirModal("Contraseñas no coinciden", "La nueva contraseña no coincide en ambos campos.", "");
                        }
                    } else {
                        abrirModal("Contraseña actual Incorrecta", "La contraseña actual no coincide con la del usuario.", "recargar");
                    }
                }
            });
        }
    });

});