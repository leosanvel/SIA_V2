$gmx(document).ready(function () {

    $("#btnGuardaSancion").click(function (event) {
        event.preventDefault();
        guardar_sancion();
    });
    // --------------------
    $("#btnBuscaSancion").click(function (event) {
        event.preventDefault();
        busca_sancion();
    });

    $("#idSancion").on("change ", function () { verifica_seleccion(); });
    


    $("#BuscaFechaInicio").datepicker({ changeYear: true, changeMonth: true });
    $("#BuscaFechaFin").datepicker({ changeYear: true, changeMonth: true });

    configuraDatepickers("FechaInicio", "FechaFin", "");

    flatpickr("#FechasFlatpickr", {
        mode: "multiple",
        dateFormat: "d/m/Y",
    });
    cargaFechasConsecutivas();
    $("#checkFechasConsecutivas").on("change", function () { cargaFechasConsecutivas(); });

});
function funcionSeleccionar() { //se ejecuta al seleccionar el empleado
    verifica_seleccion();
}
function verifica_seleccion() {

    var licencia = $("#idSancion").val()
    var empleado = $("#idPersona").val()

    if (licencia == "2") { //ARTÍCULO 37
        $("#idPorcentaje").removeClass("obligatorio");

        $("#DiasPagados1").addClass("obligatorio");
        $("#PorcentajePagado1").addClass("obligatorio");
        $("#DiasPagados2").addClass("obligatorio");
        $("#PorcentajePagado2").addClass("obligatorio");

        $("#contenedorPorcentaje").hide();

        if (empleado != "") {
            $("#contenedorDetallesDescuentos").show();
            $.ajax({
                type: "POST",
                url: "/rh/gestion-asistencias/calculo-dias-articulo-37",
                data: $("#idSancion, #idPersona").serialize(),
                success: function (respuesta) {
                    if (respuesta.Error) {
                        $("#FechaInicioPuesto").val('');

                        $("#DiasPagados1").val('');
                        $("#PorcentajePagado1").val('');
                        $("#DiasDisponibles1").val('');
                        
                        $("#DiasPagados2").val('');
                        $("#PorcentajePagado2").val('');
                        $("#DiasDisponibles2").val('');
                        abrirModal("Error", "No se pudieron calcular los descuentos del empleado.", "");
                    } else {

                        var fecha = convertirFechaParaVisualizacion(respuesta.FechaInicioPuesto);
                        $("#FechaInicioPuesto").val(fecha);
                        $("#DiasPagados1").val(respuesta.DiasPagados1);
                        $("#PorcentajePagado1").val(respuesta.PorcentajePagado1);
                        $("#DiasDisponibles1").val(respuesta.DiasDisponibles1);
                        $("#DiasPagados2").val(respuesta.DiasPagados2);
                        $("#PorcentajePagado2").val(respuesta.PorcentajePagado2);
                        $("#DiasDisponibles2").val(respuesta.DiasDisponibles2);
                    }
                }
            });

        }
    } else {
        $("#contenedorDetallesDescuentos").hide();
        $("#idPorcentaje").addClass("obligatorio");
        
        $("#DiasPagados1").removeClass("obligatorio");
        $("#PorcentajePagado1").removeClass("obligatorio");
        $("#DiasPagados2").removeClass("obligatorio");
        $("#PorcentajePagado2").removeClass("obligatorio");

        $("#contenedorPorcentaje").show();
    }
    
    if(licencia == 1){
        $("#idPorcentaje option[value='0']").hide();
        $("#idPorcentaje option[value='1']").hide();
        $("#idPorcentaje option[value='25']").hide();
        $("#idPorcentaje option[value='50']").hide();
        $("#idPorcentaje option[value='75']").hide();
        $("#idPorcentaje option[value='100']").show();
        $("#idPorcentaje").val("100");
    }

    if(licencia == 3){
        $("#idPorcentaje option[value='0']").hide();
        $("#idPorcentaje option[value='1']").show();
        $("#idPorcentaje option[value='25']").hide();
        $("#idPorcentaje option[value='50']").hide();
        $("#idPorcentaje option[value='75']").hide();
        $("#idPorcentaje option[value='100']").hide();
        $("#idPorcentaje").val("1");
    }

    if(licencia == 0){
        $("#idPorcentaje option[value='0']").show();
        $("#idPorcentaje option[value='1']").show();
        $("#idPorcentaje option[value='25']").show();
        $("#idPorcentaje option[value='50']").show();
        $("#idPorcentaje option[value='75']").show();
        $("#idPorcentaje option[value='100']").show();
        $("#idPorcentaje").val("0");
    }

}


function guardar_sancion() {

    var validaEmpleado = true;
    var existeNumeroEmpleado = $("#idPersona").length > 0;
    if (!existeNumeroEmpleado || $("#idPersona").val() === "") {
        var validaEmpleado = false;
        // campo.removeClass("form-control-error");
        $("#NumeroEmpleadoSeleccionado").addClass("form-control-error");
        $("#ENumEmp").text("Seleccione un empleado");
    }

    if (validarFormulario($("#formularioCreaSancion")).valido && validaEmpleado) {

        var FechaInicio_string = $("#FechaInicio").val();
        var FechaFin_string = $("#FechaFin").val();

        var FechaInicio_format = convertirFechaParaEnvio(FechaInicio_string);
        var FechaFin_format = convertirFechaParaEnvio(FechaFin_string);

        $("#formularioBuscaSancion input[name='fechaInicioFormateada']").remove();
        $("#formularioBuscaSancion input[name='fechaFinFormateada']").remove();

        $("#formularioCreaSancion").append('<input type="hidden" name="fechaInicioFormateada" value="' + FechaInicio_format + '">');
        $("#formularioCreaSancion").append('<input type="hidden" name="fechaFinFormateada" value="' + FechaFin_format + '">');

        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/guardar-sancion",
            data: $("#formularioCreaSancion, #idPersona").serialize(),
            success: function (data) {
                if (data.idPersona) {
                    abrirModal("Información guardada", "La sanción se creó con éxito", "recargar");
                }
            }
        });
    }

}

function busca_sancion() {
    if (!formularioVacio($("#formularioBuscaSancion"))) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/buscar-sancion",
            data: $("#formularioBuscaJustificante, #idPersona").serialize(),

            success: function (data) {
                if (data.sanciones.length > 0) {
                    console.log(data);
                    $("#EResultado").text("");
                    $("#tablaResultadosSanciones").show();
                    // Limpiar la tabla existente
                    $("#tablaResultadosSanciones tbody").empty();


                    var opcionesPorcentaje = '';
                    data.porcentajes.forEach(function (porcentaje) {
                        opcionesPorcentaje += `<option value="${porcentaje.idPorcentaje}">${porcentaje.Porcentaje}%</option>`;
                    });

                    var opcionesTipos = '';
                    data.tiposSancion.forEach(function (tiposSancion) {
                        opcionesTipos += `<option value="${tiposSancion.idTipoSancion}">${tiposSancion.TipoSancion}</option>`;
                    });


                    // Iterar sobre sanciones y agregar filas a la tabla
                    data.sanciones.forEach(function (sancion) {
                        // Formatear las fechas

                        var fechaInicioFormateada = convertirFechaParaVisualizacion(sancion.FechaInicio);
                        var fechaFinFormateada = convertirFechaParaVisualizacion(sancion.FechaFin);

                        // Agregar filas a la tabla con fechas formateadas
                        $("#tablaResultadosSanciones tbody").append(`
                        <tr>
                        <input type="hidden" id="idPersona${sancion.idSancionPersona}"
                            value="${sancion.idPersona}">
                        <td>
                            <input type="text" class="form-control"
                                id="NumEmpleado${sancion.idSancionPersona}"
                                value="${sancion.NumeroEmpleado}" style="width: 100px;" readonly>
                        </td>
                        <td>
                            <select id="sancion${sancion.idSancionPersona}"
                                name="sancion${sancion.idSancionPersona}" class="obligatorio form-control"
                                readonly disabled>
                                ${opcionesTipos}
                            </select>
                        </td>

                        <td>
                            <div class="form-group datepicker-group" style="z-index: 10;">
                                <input type="text" id="fechaInicioFormateada${sancion.idSancionPersona}"
                                     value="${fechaInicioFormateada}" class="form-control" style="width: 170px;" readonly>
                                <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                                <small id="EFechaInicio"
                                    class="etiquetaError form-text form-text-error"></small>
                            </div>
                        </td>
                        <td>
                            <div class="form-group datepicker-group" style="z-index: 1;">
                                <input type="text" id="fechaFinFormateada${sancion.idSancionPersona}"
                                     value="${fechaFinFormateada}" class="form-control" style="width: 170px;" readonly>
                                <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                                <small id="EFechaInicio"
                                    class="etiquetaError form-text form-text-error"></small>
                            </div>
                        </td>
                        <td>
                            <select id="porcentaje${sancion.idSancionPersona}"
                                name="Porcentaje${sancion.idSancionPersona}"
                                class="obligatorio form-control" readonly disabled>
                                ${opcionesPorcentaje}
                            </select>
                        </td>
                        <td><textarea rows="3" class="form-control"
                                id="descripcion${sancion.idSancionPersona}"
                                style="resize: none; width: 300px;"
                                readonly>${sancion.Descripcion}</textarea></td>

                        <td>
                            <div style="display: block;">
                                <button type="button" class="btn btn-primary oculta-empleado"
                                    id="Eliminar${sancion.idSancionPersona}"
                                    onclick="eliminar(${sancion.idSancionPersona})">Eliminar</button>
                            </div>
                        </td>
                        <td>
                            <div style="display: none;">
                                <button type="button" class="btn btn-primary oculta-empleado"
                                    id="Editar_Aceptar${sancion.idSancionPersona}"
                                    onclick="editar_aceptar(${sancion.idSancionPersona})">Editar</button>
                            </div>
                        </td>
                        <td>
                            <div style="display: block;">
                                <button type="button" class="btn btn-secondary"
                                    id="Cancelar${sancion.idSancionPersona}"
                                    onclick="cancelar('${sancion.idSancionPersona}')"
                                    style="display: none">Cancelar</button>
                            </div>
                        </td>
                    </tr>
                        `);
                        $(`#porcentaje${sancion.idSancionPersona}`).val(sancion.idPorcentaje);
                        $(`#sancion${sancion.idSancionPersona}`).val(sancion.idSancion);
                    });
                } else {
                    $("#tablaResultadosJustificantes tbody").empty();
                    $("#tablaResultadosJustificantes").hide();
                    $("#EResultado").text("No se encontraron coincidencias");
                }

            }
        });
    }
    else {
        $("#EResultado").text("Ingrese un dato para buscar coincidencias");
    }
}

function cargaFechasConsecutivas() {
    if ($("#checkFechasConsecutivas").prop("checked")) {
        $("#fechaConsecutivas").show();
        $("#FechaFin").addClass("obligatorio");
        $("#FechaInicio").addClass("obligatorio");
        $("#fechaAlternadas").hide();
        $("#FechasFlatpickr").removeClass("obligatorio");
    } else {
        $("#fechaConsecutivas").hide();
        $("#FechaInicio").removeClass("obligatorio");
        $("#FechaFin").removeClass("obligatorio");
        $("#fechaAlternadas").show();
        $("#FechasFlatpickr").addClass("obligatorio");
    }

}

function cargaPeriodo() {
    if (($("#TipoJustificante").val() === "1") || ($("#TipoJustificante").val() === "7")) {
        $("#grupoPeriodo").show();
    } else {
        $("#grupoPeriodo").hide();
    }
}

function cargarTipoJustificante() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/cargar_Tipo_Justificante",
        data: {
            "TipoProceso": $("#TipoProceso").val()
        },
        success: function (data) {
            $("#TipoJustificante").html(data);
        }
    });
}

function editar_aceptar(idSancionPersona) {
    if ($("#Editar_Aceptar" + idSancionPersona).text() == "Editar") {

        $("#sancion" + idSancionPersona).attr("disabled", false);
        $("#sancion" + idSancionPersona).attr("readonly", false);
        $("#porcentaje" + idSancionPersona).attr("disabled", false);
        $("#porcentaje" + idSancionPersona).attr("readonly", false);
        $("#fechaInicioFormateada" + idSancionPersona).attr("readonly", false);
        $("#fechaInicioFormateada" + idSancionPersona).datepicker("option", "disabled", false);
        $("#fechaFinFormateada" + idSancionPersona).attr("readonly", false);
        $("#fechaFinFormateada" + idSancionPersona).datepicker("option", "disabled", false);
        configuraDatepickers("fechaInicioFormateada", "fechaFinFormateada", idSancionPersona);

        $("#descripcion" + idSancionPersona).attr("readonly", false);

        $("#Editar_Aceptar" + idSancionPersona).text("Aceptar");
        $("#Cancelar" + idSancionPersona).toggle();
    }
    else {
        guardar_modificar_sancion(idSancionPersona);
    }
}

function cancelar(idSancionPersona) {

    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/cancela_sancion",
        data: {
            "idSancionPersona": idSancionPersona,
        },
        success: function (sancion) {

            fechaInicial = convertirFechaParaVisualizacion(sancion.FechaInicio);
            fechaFinal = convertirFechaParaVisualizacion(sancion.FechaFin);

            $("#fechaInicioFormateada" + idSancionPersona).attr("readonly", true);
            $("#fechaInicioFormateada" + idSancionPersona).datepicker("option", "disabled", true);

            $("#fechaFinFormateada" + idSancionPersona).attr("readonly", true);
            $("#fechaFinFormateada" + idSancionPersona).datepicker("option", "disabled", true);
            $("#porcentaje" + idSancionPersona).attr("readonly", true);
            $("#porcentaje" + idSancionPersona).attr("disabled", true);
            $("#sancion" + idSancionPersona).attr("readonly", true);
            $("#sancion" + idSancionPersona).attr("disabled", true);

            $("#descripcion" + idSancionPersona).attr("readonly", true);

            $("#fechaInicioFormateada" + idSancionPersona).val(fechaInicial);
            $("#fechaFinFormateada" + idSancionPersona).val(fechaFinal);
            $("#porcentaje" + idSancionPersona).val(sancion.idPorcentaje);
            $("#sancion" + idSancionPersona).val(sancion.idSancion);

            $("#Editar_Aceptar" + idSancionPersona).text("Editar");
            $("#Cancelar" + idSancionPersona).toggle();
        }
    });
}

function guardar_modificar_sancion(idSancionPersona) {
    if (!idSancionPersona) {
        index = "";
    } else {
        index = idSancionPersona;
    }

    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-asistencias/guardar-sancion",
        data: {
            "idSancionPersona": idSancionPersona,
            "idPersona": $("#idPersona" + index).val(),
            "idSancion": $("#sancion" + index).val(),
            "idPorcentaje": $("#porcentaje" + index).val(),
            "FechaInicio": $("#fechaInicioFormateada" + index).val(),
            "FechaFin": $("#fechaFinFormateada" + index).val(),
            "Descripcion": $("#descripcion" + index).val(),
            "checkFechasConsecutivas": true,
        },
        success: function (data) {
            var fechaInicioFormateada = convertirFechaParaVisualizacion(data.FechaInicio);
            var fechaFinFormateada = convertirFechaParaVisualizacion(data.FechaFin);
            cancelar(data.idSancionPersona)
        }

    });

}

function eliminar(index) {
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/eliminar-sancion",
        data: {
            "idSancionPersona": index
        },
        success: function (data) {
            if (data.eliminado) {
                abrirModal("Sancion eliminada", "La sanción se ha eliminado de manera correcta", "recargar");
            }
        }
    });
}

function configuraDatepickers(idInicio, idFin, data) {
    $(`#${idInicio}${data}, #${idFin}${data}`).datepicker({
        // $(`#fechaInicioFormateada${data}, #fechaFinFormateada${data}`).datepicker({
        changeYear: true,
        changeMonth: true,
        beforeShow: function (input, inst) {
            var fechaLimite = this.id === `${idInicio}${data}` ? $(`#${idFin}${data}`).datepicker("getDate") : $(`#${idInicio}${data}`).datepicker("getDate");
            if (this.id === `${idInicio}${data}`) {
                if (fechaLimite) {
                    $(this).datepicker("option", "maxDate", fechaLimite);
                } else {
                    //$(this).datepicker("option", "maxDate", null);
                }
            } else {
                if (fechaLimite) {
                    $(this).datepicker("option", "minDate", fechaLimite);
                }
                else {
                    //$(this).datepicker("option", "minDate", null);
                }
            }
        },
        onSelect: function (dateText) {
            var fechaInicial = $(`#${idInicio}${data}`).datepicker("getDate");
            var fechaFinal = $(`#${idFin}${data}`).datepicker("getDate");

            if (fechaFinal && fechaInicial) {
                if (fechaInicial > fechaFinal) {
                    abrirModal("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.", "");
                    $(this).val("");

                } else {
                    // var fechaInicioISO = $.datepicker.formatDate('yy-mm-dd', fechaInicial);
                    // var fechaFinISO = $.datepicker.formatDate('yy-mm-dd', fechaFinal);

                    // $.ajax({
                    //     async: false,
                    //     type: "POST",
                    //     url: "/RH/obtener_quincenas_entre_fechas",
                    //     data: {
                    //         "FechaInicio": fechaInicioISO,
                    //         "FechaFin": fechaFinISO
                    //     },
                    //     success: function (data) {
                    //         $("#NumeroQuincena").val(data)
                    //      }
                    // });
                }
            }
        }
    });
}