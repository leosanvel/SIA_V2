$(document).ready(function () {


    $("#btnBuscaUsuario").click(buscar_concepto);
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
                            <input type="text" class="form-control" id="TipoConcepto${cont}" value="${usuario.Usuario}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto${cont}" value="${usuario.Contrasenia}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto${cont}" value="${usuario.PrimerIngreso}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Abreviatura${cont}" value="${usuario.idPersona}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Porcentaje${cont}" value="${usuario.Activo}" readonly></input>
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