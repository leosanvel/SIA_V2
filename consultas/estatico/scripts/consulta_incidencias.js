$gmx(document).ready(function () {

    $("#btnConsultaIncidencia").click(function (event) {
        event.preventDefault();
        if (!formularioVacio($("#formularioBuscaIncidencia"))) {
            var BuscaFechaInicioFormateada = convertirFechaParaEnvio($("#BuscaFechaInicio").val())
            $("#formularioBuscaIncidencia input[name='BuscaFechaInicioFormateada']").remove();
            $("#formularioBuscaIncidencia").append('<input type="hidden" name="BuscaFechaInicioFormateada" value="' + BuscaFechaInicioFormateada + '">');
            var BuscaFechaFinFormateada = convertirFechaParaEnvio($("#BuscaFechaFin").val())
            $("#formularioBuscaIncidencia input[name='BuscaFechaFinFormateada']").remove();
            $("#formularioBuscaIncidencia").append('<input type="hidden" name="BuscaFechaFinFormateada" value="' + BuscaFechaFinFormateada + '">');
            $.ajax({
                async: false,
                type: "POST",
                url: "/consultas/consultar-incidencia",
                data: $("#formularioBuscaIncidencia, #idPersona").serialize(),

                success: function (data) {
                    if (data.length > 0) {
                        $("#EResultado").text("");
                        $("#tablaResultadosIncidencias").show();
                        // Limpiar la tabla existente
                        $("#tablaResultadosIncidencias tbody").empty();
                        // Iterar sobre los incidencias y agregar filas a la tabla
                        data.forEach(function (checador) {
                            // Formatear las fechas

                            var fecha = convertirFechaParaVisualizacion(checador.Fecha);



                            // Agregar filas a la tabla con fechas formateadas
                            $("#tablaResultadosIncidencias tbody").append(`
                                <tr>  
                                    <td>${checador.NumeroEmpleado}</td>
                                    <td>${fecha}</td>
                                    <td>${checador.HoraEntrada ? checador.HoraEntrada : '-'}</td>
                                    <td>${checador.HoraSalida ? checador.HoraSalida : '-'}</td>
                                    <td>${checador.idQuincenaReportada ? checador.idQuincenaReportada : '-'}</td>
                                    <td>${checador.idIncidencia ? 'Sí' : '-'}</td>
                                    <td>${checador.idJustificante ? 'Sí' : '-'}</td>
                                </tr>
                            `);

                        });
                    } else {
                        $("#tablaResultadosIncidencias tbody").empty();
                        $("#tablaResultadosIncidencias").hide();
                        $("#EResultado").text("No se encontraron coincidencias");
                    }

                }
            });
        }
        else {
            $("#EResultado").text("Ingrese un dato para buscar coincidencias");
        }
    });

    $("#BuscaFechaInicio").datepicker({ changeYear: true, changeMonth: true });
    $("#BuscaFechaFin").datepicker({ changeYear: true, changeMonth: true });
});



