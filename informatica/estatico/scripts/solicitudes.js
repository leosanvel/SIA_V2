$gmx(document).ready(function () {
    inicializacion();
    $("#btnCancelarModalAltaBaja").on("click", function () { cancelarSelectEstadoSolicitud(); });
});




function inicializacion() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/Informatica/Cargar_Solicitudes",
        success: function (data) {
            $("#TablaSolicitudes").show();
            $("#TablaSolicitudes tbody").empty();
            var opcionesEstados = '';
            data.estadosSolicitud.forEach(function (estado) {
                opcionesEstados += `<option value="${estado.idEstadoSolicitud}">${estado.Estado}</option>`;
            });
            data.Solicitudes.forEach(function (solicitud) {


                var estadoClase;
                switch (solicitud.idEstadoSolicitud) {
                    case 1:
                        estadoClase = "pendiente";
                        break;
                    case 2:
                        estadoClase = "en-progreso";
                        break;
                    case 3:
                        estadoClase = "completado";
                        break;
                    default:
                        estadoClase = "";
                }

                contenido =
                    `
                    <tr>
                    <td "> <div id="color${solicitud.idSolicitud}" class="estado-solicitud ${estadoClase}"></div> </td>
                        <td >${solicitud.Solicitud}</td>
                        <td >${solicitud.Descripcion}</td>
                        <td >
                        <select id="idEstadoSolicitud${solicitud.idSolicitud}"
                                    class="obligatorio form-control" readonly disabled>
                                    ${opcionesEstados}
                                </select>
                        </td>
                        <td>
                            <button id=btnEditar${solicitud.idSolicitud} onclick="editar_aceptar(${solicitud.idSolicitud})" class="btn btn-primary btn-sm">Editar</button>
                        </td>
                        <td>
                            <div style="display: block;">
                                <button type="button" class="btn btn-secondary"
                                    id="Cancelar${solicitud.idSolicitud}"
                                    onclick="cancelar('${solicitud.idSolicitud}')"
                                    style="display: none">Cancelar</button>
                            </div>
                        </td>
                    </tr>
                    `

                $("#TablaSolicitudes tbody").append(contenido);
                $(`#idEstadoSolicitud${solicitud.idSolicitud}`).val(solicitud.idEstadoSolicitud);
                $(`#idEstadoSolicitud${solicitud.idSolicitud}`).change(modal_completado);
            });
        }
    });
}

function modal_completado() {
    var seleccion = $(this).val();
    if (seleccion == 3) {
        $('#ModalCompletado').modal('show');
    }
}


function editar_aceptar(idSolicitud) {
    if ($("#btnEditar" + idSolicitud).text() == "Editar") {

        $("#idEstadoSolicitud" + idSolicitud).attr("disabled", false);
        $("#idEstadoSolicitud" + idSolicitud).attr("readonly", false);

        $("#btnEditar" + idSolicitud).text("Aceptar");
        $("#Cancelar" + idSolicitud).toggle();
    }
    else {
        guardar_modificar_solicitud(idSolicitud);
    }
}

function cancelar(idSolicitud) {

    $.ajax({
        async: false,
        type: "POST",
        url: "/Informatica/cancela_solicitud",
        data: {
            "idSolicitud": idSolicitud,
        },
        success: function (solicitud) {

            $("#idEstadoSolicitud" + idSolicitud).attr("readonly", true);
            $("#idEstadoSolicitud" + idSolicitud).attr("disabled", true);

            $("#idEstadoSolicitud" + idSolicitud).val(solicitud.idEstadoSolicitud);

            $("#btnEditar" + idSolicitud).text("Editar");
            $("#Cancelar" + idSolicitud).toggle();

            var estadoClase;
            switch (solicitud.idEstadoSolicitud) {
                case 1:
                    estadoClase = "pendiente";
                    break;
                case 2:
                    estadoClase = "en-progreso";
                    break;
                case 3:
                    estadoClase = "completado";
                    break;
                default:
                    estadoClase = "";
            }
            $("#color" + idSolicitud).removeClass()
            $("#color" + idSolicitud).addClass("estado-solicitud")
            $("#color" + idSolicitud).addClass(estadoClase)

        }
    });
}

function guardar_modificar_solicitud(idSolicitud) {
    $.ajax({
        async: false,
        type: "POST",
        url: "/Informatica/guardaSolicitud",
        data: {
            "idSolicitud": idSolicitud,
            "idEstadoSolicitud": $("#idEstadoSolicitud" + idSolicitud).val(),
        },
        success: function (data) {
            cancelar(data.idSolicitud)
        }

    });

}