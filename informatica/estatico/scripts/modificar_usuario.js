$(document).ready(function () {


    $("#btnBuscaUsuario").click(buscar_concepto);
    // $("#btnCrearUsuarioModal").on("click", function (event) { crear_usuario(); });
    $("#btnCrearUsuarioModal").click(crear_usuario);
});

function buscar_concepto() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/informatica/gestion-usuarios/buscar-usuario",
        data: $("#BuscarUsuario").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
            } else {
                $("#tablaResultadoUsuarios").show();
                $("#tablaResultadoUsuarios tbody").empty();
                var cont = 1;
                data.forEach(function (usuario) {
                    text = `
                    <tr>
                        
                        <td>
                            <input type="text" class="form-control" id="Usuario${cont}" value="${usuario.Usuario}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Contrasenia${cont}" value="${usuario.Contrasenia}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="PrimerIngreso${cont}" value="${usuario.PrimerIngreso}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idPersona${cont}" value="${usuario.idPersona}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Activo${cont}" value="${usuario.Activo}" readonly></input>
                        </td>
                        <td>
                        <div>
                        <button type="button" class="btn btn-primary btn-sm" id="Editar_Aceptar${cont}" onclick="modal_editar_elemento(${cont})"> <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span> </button>
                        </div>
                        </td>

                    </tr>
                    `;
                    cont++;
                    $("#tablaResultadoUsuarios tbody").append(text);
                });
            }
        }
    })

}


function modal_editar_elemento(consecutivo) {

    $('#ModalAgregarUsuario').modal('show');

}

function crear_usuario() {
    
    if (validarFormulario($("#frmCreaUsuario")).valido) {
        // Serializar los datos del formulario
        var formData = $("#frmCreaUsuario").serializeArray();
        
        var checkboxStates = getCheckboxStates();
        // Añadir los datos de checkboxStates al formData
        formData.push({ name: 'checkboxStates', value: JSON.stringify(checkboxStates) });

        $.ajax({
            type: "POST",
            url: "/informatica/gestion-usuarios/crear-usuario",
            data: $.param(formData),  // Serializar formData a una cadena de consulta
            success: function (data) {
                if (data.Error) {
                    abrirModal("Error", "ERROR.", "");
                } else {
                    abrirModal("Cambios efectuados", "Los cambios se han realizado correctamente.", "");
                }
            }
        });
    }
}
