$gmx(document).ready(function () {
    $("#btnEnviarNomina").click(abrirAdModal);
    $("#btnVistaPrevia").click(vistaPrevia);
    $("#btnCerrarVistaPrevia").click(CerrarVistaPrevia);
    $("#btnGenerarNomina").click(generaReporteIncidencias);
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
            url: "/Nomina/vistaprevia",
            data: $("#formularioEnviarNomina").serialize(),
            success: function (data) {
                
                if (data.NoChecador) {
                    abrirModal("Checador no generado", "La operación no esta disponible porque no se ha generado el checador de esta quincena", "recargar");
                }
                else if (data.NoPersonas) {
                    abrirModal("No hay empleados activos", "No se encontraron empleados", "recargar");
                }
                else if (data.NoCoincidencias) {
                    abrirModal("No hay coincidencias", "No existe un registro checador para los empleados activos", "recargar");
                }
                else if (data.NoIncidencias) {
                    abrirModal("No hay incidencias", "No se encontraron incidencias", "recargar");
                }
    
                if (data.Existente) {
                    abrirModal("La nómina ya fue reportada", `El documento ya existe`, "");
                }
    
                if(data.Existente || data.Creado){
                    $("#tablaVistaPrevia tbody").empty();
                    data.lista_nomina.forEach(function (Nomina) {
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
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/generaReporteIncidencias",
        data: $("#formularioEnviarNomina").serialize(),
        success: function (data) {

            if (data.NoChecador) {
                abrirModal("Checador no generado", "La operación no esta disponible porque no se ha generado el checador de esta quincena", "recargar");
            }
            else if (data.NoPersonas) {
                abrirModal("No hay empleados activos", "No se encontraron empleados", "recargar");
            }
            else if (data.NoCoincidencias) {
                abrirModal("No hay coincidencias", "No existe un registro checador para los empleados activos", "recargar");
            }
            else if (data.NoIncidencias) {
                abrirModal("No hay incidencias", "No se encontraron incidencias", "recargar");
            }

            if (data.Creado) {
                abrirModal("Documento generado", "El reporte ha sido creado correctamente", "");
            }
            else if (data.Existente) {
                abrirModal("La nómina ya existe", `El documento ya existe`, "");
            }

            if(data.Existente || data.Creado){
                // Manejar la respuesta JSON para obtener la URL de descarga
                var urlDescarga = data.url_descarga;
                $("#btnDescargaDocumento").show();
                // Crear un enlace de descarga dinámico
                $("#btnDescargaDocumento").wrap('<a href="' + urlDescarga + '" download></a>');
            }

        }
    });
}