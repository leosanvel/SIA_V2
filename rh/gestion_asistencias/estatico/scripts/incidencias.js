$gmx(document).ready(function () {


    cargarTipoIncidencia();



    $("#btnGuardaIncidencia").click(function (event) {
        event.preventDefault();

        if (validarFormulario($("#formularioCreaIncidencia")).valido) {
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-asistencias/guardar-incidencia",
                data: $("#formularioCreaIncidencia, #idPersona").serialize(),
                success: function (data) {
                    if (data.idPersona) {
                        abrirModal("Información guardada", "La incidencia se creó con éxito", "recargar");
                    }
                    else {
                        abrirModal("Política inexistente", "La incidencia no está en las políticas del personal", "");
                    }
                }
            });
        }
    });

    $("#btnBuscaIncidencia").click(function (event) {
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
                url: "/rh/gestion-asistencias/buscar-incidencia",
                data: $("#formularioBuscaIncidencia, #idPersona").serialize(),

                success: function (data) {
                    if (data.length > 0) {
                        $("#EResultado").text("");
                        $("#tablaResultadosIncidencias").show();
                        // Limpiar la tabla existente
                        $("#tablaResultadosIncidencias tbody").empty();
                        // Iterar sobre los incidencias y agregar filas a la tabla
                        data.forEach(function (incidencia) {
                            // Formatear las fechas

                            var fechaInicioFormateada = convertirFechaParaVisualizacion(incidencia.FechaInicio);
                            var fechaFinFormateada = convertirFechaParaVisualizacion(incidencia.FechaFin);

                            // Agregar filas a la tabla con fechas formateadas
                            $("#tablaResultadosIncidencias tbody").append(`
                                <tr>  
                                <td><input type="text" class="form-control" id="NumEmpleado${incidencia.idIncidencia}" value="${incidencia.NumeroEmpleado}" style="width: 100px;" readonly></td>    
                                <input type="hidden" id="idPersona${incidencia.idIncidencia}" value="${incidencia.idPersona}">
                                <td>
                                    <div class="form-group datepicker-group"  style="z-index: 10;">
                                        <input type="text" id="fechaInicioFormateada${incidencia.idIncidencia}"
                                        class="form-control" value="${fechaInicioFormateada}" readonly>
                                        <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                                        <small id="EFechaInicio" class="etiquetaError form-text form-text-error"></small>
                                    </div>
                                </td>  
                                <td>
                                    <div class="form-group datepicker-group"  style="z-index: 1;">
                                        <input type="text" id="fechaFinFormateada${incidencia.idIncidencia}"
                                        class="form-control" value="${fechaFinFormateada}" readonly>
                                        <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                                        <small id="EFechaInicio" class="etiquetaError form-text form-text-error"></small>
                                    </div>
                                </td>  
                                <td><textarea rows="3" class="form-control" id="descripcion${incidencia.idIncidencia}" style="resize: none; width: 300px;" readonly>${incidencia.Descripcion}</textarea></td>   

                                <td>
                                    <div style="display: block;">
                                        <button type="button" class="btn btn-primary oculta-empleado" id="Eliminar${incidencia.idIncidencia}" onclick="eliminar(${incidencia.idIncidencia})">Eliminar</button>
                                    </div>
                                </td>

                                <td>
                                <div style="display: block;">
                                    <button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar${incidencia.idIncidencia}" onclick="editar_aceptar(${incidencia.idIncidencia})">Editar</button>
                                </div>
                            </td>
                            <td>
                                <div style="display: block;">
                                    <button type="button" class="btn btn-secondary" id="Cancelar${incidencia.idIncidencia}" onclick="cancelar('${incidencia.idIncidencia}')" style="display: none">Cancelar</button>
                                </div>
                            </td>
                             </tr>
                                <input type="hidden" id="TipoIncidencia${incidencia.idIncidencia}" value="${incidencia.idTipo}">
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

    configuraDatepickers("fechaInicio", "fechaFin", "");
    flatpickr("#FechasFlatpickr", {
        mode: "multiple",
        dateFormat: "d/m/Y",
    });
    cargaFechasConsecutivas();
    $("#checkFechasConsecutivas").on("change", function () { cargaFechasConsecutivas(); });
});

function cargaFechasConsecutivas() {
    if ($("#checkFechasConsecutivas").prop("checked")) {
        $("#fechaConsecutivas").show();
        $("#fechaFin").addClass("obligatorio");
        $("#fechaInicio").addClass("obligatorio");
        $("#fechaAlternadas").hide();
        $("#FechasFlatpickr").removeClass("obligatorio");
    } else {
        $("#fechaConsecutivas").hide();
        $("#fechaInicio").removeClass("obligatorio");
        $("#fechaFin").removeClass("obligatorio");
        $("#fechaAlternadas").show();
        $("#FechasFlatpickr").addClass("obligatorio");
    }

}

function cargarTipoIncidencia() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/cargar-tipo-incidencia",
        success: function (data) {
            $("#TipoIncidencia").html(data);
        }
    });
}

function editar_aceptar(data) {
    if ($("#Editar_Aceptar" + data).text() == "Editar") {

        $("#descripcion" + data).attr("readonly", false);
        $("#fechaInicioFormateada" + data).prop("readonly", false);
        $("#fechaInicioFormateada" + data).datepicker("option", "disabled", false);
        $("#fechaFinFormateada" + data).prop("readonly", false);
        $("#fechaFinFormateada" + data).datepicker("option", "disabled", false);
        configuraDatepickers("fechaInicioFormateada", "fechaFinFormateada", data);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else {
        guardar_modificar_incidencia(data);
    }
}

function cancelar(idIncidencia) {

    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-asistencias/cancelar-incidencia",
        data: {
            "idIncidencia": idIncidencia,
        },
        success: function (incidencia) {

            fechaInicial = convertirFechaParaVisualizacion(incidencia.FechaInicio);
            fechaFinal = convertirFechaParaVisualizacion(incidencia.FechaFin);

            $("#fechaInicioFormateada" + idIncidencia).attr("readonly", true);
            $("#fechaInicioFormateada" + idIncidencia).datepicker("option", "disabled", true);
            $("#fechaFinFormateada" + idIncidencia).attr("readonly", true);
            $("#fechaFinFormateada" + idIncidencia).datepicker("option", "disabled", true);
            $("#descripcion" + idIncidencia).attr("readonly", true);

            $("#fechaInicioFormateada" + idIncidencia).val(fechaInicial);
            $("#fechaFinFormateada" + idIncidencia).val(fechaFinal);
            $("#descripcion" + idIncidencia).val(incidencia.Descripcion);

            $("#Editar_Aceptar" + idIncidencia).text("Editar");
            $("#Cancelar" + idIncidencia).toggle();
        }
    });
}

function guardar_modificar_incidencia(dato) {
    if (!dato) {
        index = "";
    } else {
        index = dato;
    }
    var descripcionIncidencia = $("#descripcion" + index).val();
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-asistencias/guardar-incidencia",
        data: {

            "idIncidencia": dato,
            "idPersona": $("#idPersona" + index).val(),
            "Descripcion": descripcionIncidencia,
            "TipoIncidencia": $("#TipoIncidencia" + index).val(),
            "fechaInicio": $("#fechaInicioFormateada" + index).val(),
            "fechaFin": $("#fechaFinFormateada" + index).val(),
            "checkFechasConsecutivas": true,
        },
        success: function (data) {
            var fechaInicioFormateada = convertirFechaParaVisualizacion(data.fechaInicio);
            var fechaFinFormateada = convertirFechaParaVisualizacion(data.fechaFin);
            cancelar(data.idIncidencia);
        }

    });

}

function eliminar(index) {
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-asistencias/eliminar-incidencia",
        data: {
            "idIncidencia": index
        },
        success: function (data) {
            if(data.eliminado){
                abrirModal("Incidencia eliminada", "La incidencia se ha eliminado de manera correcta", "recargar");
            }
        }
    });
}

function configuraDatepickers(idInicio, idFin, data, FechaInicio, FechaFin) {
    $(`#${idInicio}${data}, #${idFin}${data}`).datepicker({
        // $(`#fechaInicioFormateada${data}, #fechaFinFormateada${data}`).datepicker({
        changeYear: true,
        changeMonth: true,
        beforeShow: function (input, inst) {
            var fechaLimite = this.id === `${idInicio}${data}` ? $(`#${idFin}${data}`).datepicker("getDate") : $(`#${idInicio}${data}`).datepicker("getDate");
            if (this.id === `${idInicio}${data}`) {
                if (fechaLimite) {
                    $(this).datepicker("option", "maxDate", fechaLimite);
                    console.log(typeof (fechaLimite));
                } else {
                    //$(this).datepicker("option", "maxDate", FechaFin);
                }
            } else {
                if (fechaLimite) {
                    $(this).datepicker("option", "minDate", fechaLimite);
                }
                else {
                    //$(this).datepicker("option", "minDate", FechaInicio);
                }
            }
        },
        onSelect: function (dateText) {
            var fechaFinal = $(`#${idFin}${data}`).datepicker("getDate");
            var fechaInicial = $(`#${idInicio}${data}`).datepicker("getDate");

            if ((fechaFinal && fechaInicial) && (fechaInicial > fechaFinal)) {
                abrirModal("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.", "");
                $(this).val("");
            }
        }
    });
}