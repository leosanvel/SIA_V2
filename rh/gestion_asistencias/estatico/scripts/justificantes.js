$gmx(document).ready(function () {

    //$(document).on('click', "input:checkbox", un_solo_checkbox);

    $("#TipoProceso").change(function (event) {
        event.preventDefault();
        var TipoProceso = $("#TipoProceso").val();
        if (TipoProceso === "2") {
            $("#NumEmpGrupo").hide();
            $("#idPersona").val("");
            $("#tablaEmpleadoSeleccionado").hide();
        } else if (TipoProceso === "1") {
            $("#NumEmpGrupo").show();
            if ($("#idPersona").val()) {
                $("#tablaEmpleadoSeleccionado").show();
            }
        }
        cargarTipoJustificante();
        cargaPeriodo();
    });

    cargarTipoJustificante();
    cargaPeriodo();

    $("#TipoJustificante").change(function (event) { sel_vacaciones(); });


    $("#btnGuardaJustificante").click(function (event) {
        event.preventDefault();

        var validaEmpleado = true;
        if ($("#TipoProceso").val() == 1) {
            var existeNumeroEmpleado = $("#idPersona").length > 0;
            if (!existeNumeroEmpleado || $("#idPersona").val() === "") {
                var validaEmpleado = false;
                // campo.removeClass("form-control-error");
                $("#NumeroEmpleadoSeleccionado").addClass("form-control-error");
                $("#ENumEmp").text("Seleccione un empleado");
            }
        } else {
            $("#idPersona").val("");
        }

        var dias_adecuados = true;
        var dias_adecuados = true;
        var al_menos_uno = true;
        $("#ESeleccionPeriodos").text("");

        //datos = $("#formularioCreaJustificante, #TipoProceso, #idPersona").serialize();

        datos = new FormData($("#formularioCreaJustificante")[0]);
        datos.append('idPersona', $("#idPersona").val());
        datos.append('TipoProceso', $("#TipoProceso").val());

        if ($("#TipoJustificante").val() == 7) {

            if ($("#checkFechasConsecutivas").prop("checked")) {
                var FechaInicio_string = $("#fechaInicio").val();
                var FechaFin_string = $("#fechaFin").val();

                var FechaInicio_format = convertirFechaParaEnvio(FechaInicio_string);
                var FechaFin_format = convertirFechaParaEnvio(FechaFin_string);

                FechaInicio_format = new Date(FechaInicio_format);
                FechaFin_format = new Date(FechaFin_format);

                dias = FechaFin_format - FechaInicio_format;
                dias = Math.floor(dias / (1000 * 60 * 60 * 24)) + 1;
            } else {
                fechas = $("#FechasFlatpickr").val().split(",");
                dias = fechas.length;
            }

            const arrayId = $('[name="id[]"]:checked').map(function () {
                return this.value;
            }).get();
            console.log(arrayId);
            if(arrayId.length > 0){
                var arrayDias = $(".input-valor input[type=text], .input-valor").map(function () {
                    if ($.inArray($(this).attr("data-chbxvalue"), arrayId) != -1) {
                        return $(this).val();
                    }
                }).get();
                var arrayidPeriodo = $('input[id^=Periodo]').map(function () {
                    if ($.inArray($(this).attr("data-chbxvalue"), arrayId) != -1) {
                        return $(this).val();
                    }
                }).get();
                var arrayFecha = $('input[id^=Fecha]').map(function () {
                    if ($.inArray($(this).attr("data-chbxvalue"), arrayId) != -1) {
                        return $(this).val();
                    }
                }).get();
                console.log(arrayFecha);
                dias_total = 0;
                arrayDias.forEach(function (dia) {
                    dias_total += Number(dia);
                });
    
                if (dias > dias_total) {
                    dias_adecuados = false;
                }
                datos.append("listaDias", arrayDias);
                datos.append("listaPeriodo", arrayidPeriodo);
                datos.append("listaFecha", arrayFecha);
            }else{
                $("#ESeleccionPeriodos").text("No se selecciono al menos un periodo.");
                al_menos_uno = false;
            }
        }

        if (validarFormulario($("#formularioCreaJustificante")) && validaEmpleado && dias_adecuados && al_menos_uno) {
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-asistencias/guardar-justificante",
                data: datos,
                enctype: 'multipart/form-data',
                contentType: false,
                processData: false,
                success: function (data) {
                    if (data.idPersona) {
                        abrirModal("Información guardada", "El justificante se creó con éxito", "recargar");
                    }
                }
            });
        }
    });

    $("#btnBuscaJustificante").click(function (event) {
        event.preventDefault();
        if (!formularioVacio($("#formularioBuscaJustificante"))) {
            var BuscaFechaInicioFormateada = convertirFechaParaEnvio($("#BuscaFechaInicio").val())
            $("#formularioBuscaJustificante input[name='BuscaFechaInicioFormateada']").remove();
            $("#formularioBuscaJustificante").append('<input type="hidden" name="BuscaFechaInicioFormateada" value="' + BuscaFechaInicioFormateada + '">');
            var BuscaFechaFinFormateada = convertirFechaParaEnvio($("#BuscaFechaFin").val())
            $("#formularioBuscaJustificante input[name='BuscaFechaFinFormateada']").remove();
            $("#formularioBuscaJustificante").append('<input type="hidden" name="BuscaFechaFinFormateada" value="' + BuscaFechaFinFormateada + '">');
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-asistencias/buscar-justificante",
                data: $("#formularioBuscaJustificante, #idPersona").serialize(),

                success: function (data) {
                    if (data.length > 0) {
                        $("#EResultado").text("");
                        $("#tablaResultadosJustificantes").show();
                        // Limpiar la tabla existente
                        $("#tablaResultadosJustificantes tbody").empty();
                        // Iterar sobre los justificantes y agregar filas a la tabla
                        data.forEach(function (justificante) {
                            // Formatear las fechas

                            var fechaInicioFormateada = convertirFechaParaVisualizacion(justificante.FechaInicio);
                            var fechaFinFormateada = convertirFechaParaVisualizacion(justificante.FechaFin);

                            // Agregar filas a la tabla con fechas formateadas
                            $("#tablaResultadosJustificantes tbody").append(`
                                <tr>  
                                <td><input type="text" class="form-control" id="NumEmpleado${justificante.idJustificante}" value="${justificante.NumeroEmpleado}" style="width: 100px;" readonly></td>    
                                <input type="hidden" id="idPersona${justificante.idJustificante}" value="${justificante.idPersona}">
                                <td>
                                    <div class="form-group datepicker-group"  style="z-index: 10;">
                                        <input type="text" id="fechaInicioFormateada${justificante.idJustificante}"
                                        class="form-control" value="${fechaInicioFormateada}" readonly>
                                        <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                                        <small id="EFechaInicio" class="etiquetaError form-text form-text-error"></small>
                                    </div>
                                </td>  
                                <td>
                                    <div class="form-group datepicker-group"  style="z-index: 1;">
                                        <input type="text" id="fechaFinFormateada${justificante.idJustificante}"
                                        class="form-control" value="${fechaFinFormateada}" readonly>
                                        <span class="glyphicon glyphicon-calendar" aria-hidden="true"></span>
                                        <small id="EFechaInicio" class="etiquetaError form-text form-text-error"></small>
                                    </div>
                                </td>  
                                <td><textarea rows="3" class="form-control" id="descripcion${justificante.idJustificante}" style="resize: none; width: 300px;" readonly>${justificante.Descripcion}</textarea></td>   
                                
                                <td>
                                    <div style="display: block;">
                                        <button type="button" class="btn btn-primary oculta-empleado" id="Eliminar${justificante.idJustificante}" onclick="eliminar(${justificante.idJustificante})">Eliminar</button>
                                    </div>
                                </td>

                                <td>
                                <div style="display: block;">
                                    <button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar${justificante.idJustificante}" onclick="editar_aceptar(${justificante.idJustificante})">Editar</button>
                                </div>
                            </td>
                            <td>
                                <div style="display: block;">
                                    <button type="button" class="btn btn-secondary" id="Cancelar${justificante.idJustificante}" onclick="cancelar('${justificante.idJustificante}')" style="display: none">Cancelar</button>
                                </div>
                            </td>
                             </tr>
                                <input type="hidden" id="TipoJustificante${justificante.idJustificante}" value="${justificante.idTipo}">
                            `);

                        });
                        //actualizarVisibilidadElementos();
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
    });

    $("#BuscaFechaInicio").datepicker({ changeYear: true, changeMonth: true });
    $("#BuscaFechaFin").datepicker({ changeYear: true, changeMonth: true });

    $("#btnBuscaPeriodos").click(obtener_periodos);

    $("#btnBuscaPeriodos").click(obtener_periodos);

    configuraDatepickers("FechaInicio", "FechaFin", "");

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
        url: "/cargar-tipo-justificante",
        data: {
            "TipoProceso": $("#TipoProceso").val()
        },
        success: function (data) {
            $("#TipoJustificante").html(data);
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
        guardar_modificar_justificante(data);
    }
}

function cancelar(idJustificante) {

    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-asistencias/cancela-justificante",
        data: {
            "idJustificante": idJustificante,
        },
        success: function (Justificante) {

            fechaInicial = convertirFechaParaVisualizacion(Justificante.FechaInicio);
            fechaFinal = convertirFechaParaVisualizacion(Justificante.FechaFin);

            $("#fechaInicioFormateada" + idJustificante).attr("readonly", true);
            $("#fechaInicioFormateada" + idJustificante).datepicker("option", "disabled", true);
            $("#fechaFinFormateada" + idJustificante).attr("readonly", true);
            $("#fechaFinFormateada" + idJustificante).datepicker("option", "disabled", true);
            $("#descripcion" + idJustificante).attr("readonly", true);

            $("#fechaInicioFormateada" + idJustificante).val(fechaInicial);
            $("#fechaFinFormateada" + idJustificante).val(fechaFinal);
            $("#descripcion" + idJustificante).val(Justificante.Descripcion);

            $("#Editar_Aceptar" + idJustificante).text("Editar");
            $("#Cancelar" + idJustificante).toggle();
        }
    });
}

function sel_vacaciones() {
    if ($("#TipoJustificante").val() == 7) {
        $("#btnBuscaPeriodos").show();
    } else {
        $("#btnBuscaPeriodos").hide();
    }
}

function obtener_periodos() {
    if ($("#NumeroEmpleadoSeleccionado").val() != "") {
        $("#tabPeriodos").show();

        $.ajax({
            async: false,
            type: "POST",
            url: "/RH/obtenerDiasPersona",
            data: {
                "idPersona": $("#idPersona").val()
            },
            success: function (data) {
                if (data.length > 0) {
                    $("#EResultadoPeriodos").text("");
                    var cont = 1;
                    $("#tabPeriodos tbody").empty();
                    data.forEach(function (DiasPersona) {
                        var Fecha = convertirFechaParaVisualizacion(DiasPersona.Fecha)

                        var text = `
                        <tr>
                            <td><input type="checkbox" name="id[]" id="check${cont}" value="${cont}">
                            <input type="text" class="form-control" id="idPersona${cont}" value=${DiasPersona.idPersona} data-chbxvalue="${cont}" readonly style="display: none;"></td>
                            <td><input type="text" class="form-control" id="Periodo${cont}" value=${DiasPersona.idPeriodo} data-chbxvalue="${cont}" readonly></td>
                            <td><input type="text" class="form-control input-valor" id="DiasGanados${cont}" name="valor[]" value="${DiasPersona.DiasGanados}" data-chbxvalue="${cont}" readonly></td>
                            <td><input type="text" class="form-control" id="Fecha${cont}" value="${Fecha}" data-chbxvalue="${cont}" readonly></td>
                        </tr>
                        `;
                        cont++;
                        $("#tabPeriodos tbody").append(text);
                    });
                }else{
                    $("#tabPeriodos tbody").empty();
                    $("#tabPeriodos").hide();
                    $("#EResultadoPeriodos").text("No se encontraron coincidencias.");
                }
            }
        });
    }else{
        $("#EResultadoPeriodos").text("Ingrese No. de empleado para buscar coincidencias.");
    }
}

function guardar_modificar_justificante(dato) {
    if (!dato) {
        index = "";
    } else {
        index = dato;
    }


    var descripcionJustificante = $("#descripcion" + index).val();

    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-asistencias/guardar-justificante",
        data: {

            "idJustificante": dato,
            "idPersona": $("#idPersona" + index).val(),
            "Descripcion": descripcionJustificante,
            "TipoJustificante": $("#TipoJustificante" + index).val(),
            "FechaInicio": $("#fechaInicioFormateada" + index).val(),
            "FechaFin": $("#fechaFinFormateada" + index).val(),
            "checkFechasConsecutivas": true,
        },
        success: function (data) {
            cancelar(data.idJustificante);
        }

    });

}

function eliminar(index) {
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-asistencias/eliminar-justificante",
        data: {
            "idJustificante": index
        },
        success: function (data) {
            if(data.eliminado){
                abrirModal("Justificante eliminado", "El justificante se ha eliminado de manera correcta", "recargar");
            }
        }
    });
}

function un_solo_checkbox() {

    var $box = $(this);
    if ($box.is(":checked")) {
        var group = "input:checkbox[name='" + $box.attr("name") + "']";
        $(group).prop("checked", false);
        $box.prop("checked", true);
    } else {
        $box.prop("checked", false);
    }
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