$gmx(document).ready(function () {
    $("#btnEnviarNomina").click(abrirAdModal);
    $("#btnVistaPrevia").click(vistaPrevia);
    $("#btnCerrarVistaPrevia").click(CerrarVistaPrevia);
    //$("#btnGenerarReporteIncidencia").click(generaReporteIncidencias);
    $("#btnGenerarReporteIncidencia").click(ProcesandoArchivoIncidencias);
});

function abrirAdModal() {
    if (validarFormulario($("#formularioEnviarNomina")).valido) {
        $("#MensajeAdModal").html("Esta seguro de enviar nómina de la quincena " + $("#NumQuincena").val());
        $("#EnviarNominaModal").modal('show');
    }
}

function vistaPrevia() {
    if (validarFormulario($("#formularioEnviarNomina")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/vista-previa",
            data: $("#formularioEnviarNomina").serialize(),
            success: function (data) {
                console.log(data);
                if (data.NoIncidencias) {
                    abrirModal("No hay incidencias", "No se encontraron incidencias para vista previa", "recargar");
                }
                else if (data.NoChecador) {
                    abrirModal("Checador no generado", "La vista previa no esta disponible porque no se ha generado el checador de esta quincena", "recargar");
                }
                else {
                    $("#tablaVistaPrevia tbody").empty();
                    var incidencias = data.lista_nomina;
                    incidencias.forEach(function (Nomina) {
                        text = `
                            <tr>
                                <td><input type="text" class="form-control" value="${Nomina.NumeroQuincena}" readonly></td>
                                <td><input type="text" class="form-control" value="${Nomina.NumeroEmpleado}" readonly></td>
                                <td><input type="text" class="form-control" value="${Nomina.NombrePersona}" readonly></td>
                                <td><input type="text" class="form-control" value="${Nomina.DiasIncidencias}" readonly></td>
                            </tr>
                        `;
                        $("#tablaVistaPrevia tbody").append(text);
                    });
                    $("#btnCerrarVistaPrevia").toggle();
                    $("#tablaVistaPrevia").show();
                }
            }
        });
    }
}

function CerrarVistaPrevia() {
    $("#tablaVistaPrevia").hide();
    $("#btnCerrarVistaPrevia").toggle();
}


function generaReporteIncidencias() {
    if(validarFormulario($("#formularioEnviarNomina")).valido){
        window.document.getElementById("NumQuincena").disabled = "";
        window.document.getElementById("TipoEmpleado").disabled = "";
        window.document.getElementById("btnGenerarReporteIncidencia").disabled = "";
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/generar-reporte-incidencias",
            data: $("#formularioEnviarNomina").serialize(),
            success: function (data) {
                window.document.getElementById("ImgModal").style.display = "none";
                if (data.NoIncidencias) {
                    abrirModal("No hay incidencias", "No se encontraron incidencias", "recargar");
                }
                else if (data.NoChecador) {
                    abrirModal("Checador no generado", "La operación no esta disponible porque no se ha generado el checador de esta quincena", "recargar");
                }
                else {

                    if (data.respuesta == "creado") {
                        $("#EnviarNominaModal").modal('hide');
                        abrirModal("Documento generado", `El reporte ha sido creado correctamente`, "");
                    }
                    else if (data.respuesta == "existente") {
                        $("#EnviarNominaModal").modal('hide');
                        abrirModal("La nómina ya existe", `El documento ya existe`, "");
                    }
                    // Manejar la respuesta JSON para obtener la URL de descarga
                    var urlDescarga = data.url_descarga;
                    $("#btnDescargaDocumento").show();
                    // Crear un enlace de descarga dinámico
                    $("#btnDescargaDocumento").wrap('<a href="' + urlDescarga + '" download></a>');
                }
            }
        });
    }
}

function ProcesandoArchivoIncidencias(){
    $("#btnDescargar").hide();
    window.document.getElementById("NumQuincena").disabled = "disabled";
    window.document.getElementById("TipoEmpleado").disabled = "disabled";
    window.document.getElementById("btnGenerarReporteIncidencia").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generaReporteIncidencias, 2000);
}