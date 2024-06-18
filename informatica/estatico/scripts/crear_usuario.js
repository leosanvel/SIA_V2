$(document).ready(function () {


    $("#btnBuscarUsuario").click(buscar_usuario);
    // $("#btnCrearUsuarioModal").on("click", function (event) { crear_usuario(); });
    $("#btnCrearUsuarioModal").click(crear_usuario);
    $("#btnNuevoUsuario").on("click", function (event) { modal_editar_elemento(); });
});

function buscar_usuario() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/informatica/gestion-usuarios/buscar-usuario",
        data: $("#BuscarUsuario, #idPersona").serialize(),
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
                            <input type="hidden" id="idPersona${cont}" value="${usuario.idPersona}"></input>
                            <input type="text" class="form-control" id="NumeroEmpleado${cont}" value="${usuario.NumeroEmpleado}" readonly></input>
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

    if (consecutivo != undefined) { // EDITAR
        
        $('#tituloModalAgregarUsuario')[0].textContent = "Modificar usuario";
        $('#btnCrearUsuarioModal')[0].textContent = "Modificar";
        $('#btnEliminarUsuario').show();
        $('#ContenedorEstado').show();
        
        $("#NumeroEmpleadoModal").val($("#NumeroEmpleado" + consecutivo).val());
        $("#ModalUsuario").val($("#Usuario" + consecutivo).val());
        $("#ModalContrasena").val($("#Contrasenia" + consecutivo).val());
        $("#ModalEstado").val($("#Activo" + consecutivo).val());
        $("#editar").val(true);

        actualizarEstadoCheckboxes(consecutivo);
        
        // $("#NumeroEmpleadoModal").val(consecutivo);
        
        
    } else { //CREAR
        $("#editar").val(false);
        $('#tituloModalAgregarUsuario')[0].textContent = "Crear usuario";
        $('#btnCrearUsuarioModal')[0].textContent = "Crear";
        $('#btnEliminarUsuario').hide();
        $('#ContenedorEstado').hide();

        $("#NumeroEmpleadoModal").val($("#NumeroBuscarEmpleado").val());
        $("#ModalUsuario").val($("#BuscarUsuario").val());
        $("#ModalContrasena").val("");
        $("#ModalEstado").val(1);
    }

}

function crear_usuario() {

    if (validarFormulario($("#frmCreaUsuario")).valido) {
        // Serializar los datos del formulario
        var formData = $("#frmCreaUsuario").serializeArray();

        var estadosCheckbox = leerEstadosCheckbox();

        idPersona = $("#idPersona").val();
        formData.push({ name: 'idPersona', value: idPersona });
        // Añadir los datos de estadosCheckbox al formData
        formData.push({ name: 'estadosCheckbox', value: JSON.stringify(estadosCheckbox) });

        $.ajax({
            type: "POST",
            url: "/informatica/gestion-usuarios/crear-usuario",
            data: $.param(formData),  // Serializar formData a una cadena de consulta
            success: function (data) {


                if (data.editado) {
                    abrirModal("Edición completa", "La cuenta ha sido modificada.", "recargar");
                }
                if(data.existente) {
                    abrirModal("Usuario existente", "El usuario ya existe. Intente con otro nombre.", "");
                }
                if(data.creado) {
                    abrirModal("Usuario creado", "El usuario ha sido creado.", "cerrar_modales");
                }
            }
        });
    }
}

