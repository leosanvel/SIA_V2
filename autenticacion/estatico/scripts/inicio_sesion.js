$gmx(document).ready(function() {
    $("#frmUsuario").submit(function(event) {
        event.preventDefault();
        if (validarFormulario($("#frmUsuario")).valido) {
          $.ajax({
            type: "POST",
            url: "/login",
            data: $("#frmUsuario").serialize(),
            success: function(data) {
                if (data.logged === true) {
                  window.location.href = "/Principal/SIA";
                  $("#AlertaError").hide();
                }else if (data.logged === "Inactivo") {
                    // <div class="alert alert-danger" id="AlertaError" style="display: none;" role="alert"><strong>Error:</strong> verificar los campos capturados.</div>
                $("#AlertaError").html('<strong>Error:</strong> USUARIO INACTIVO');
                $("#AlertaError").show();
            }else if (data.logged === "ContrasenaIncorrecta"){
                $("#AlertaError").html('<strong>Error:</strong> Contraseña incorrecta');
                $("#AlertaError").show();
            }else if (data.logged === "UsuarioIncorrecto"){
                $("#AlertaError").html('<strong>Error:</strong> Usuario incorrecto');
                $("#AlertaError").show();
              }
            }
          });
        }
      });

});