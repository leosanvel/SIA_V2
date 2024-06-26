$gmx(document).ready(function () {

    $("#FechaInicioContrato").datepicker({
        changeYear: true,
        changeMonth: true,
        container: '.modal' // Esto colocará el calendario dentro del elemento con la clase "modal"
    });

    $("#FechaFinContrato").datepicker({ changeYear: true, changeMonth: true });

    $("#btnBuscaEmpleadoConcepto").click(buscar_empleado_concepto);
    $("#btnCrearEmpleadoConcepto").click(crear_empleado_concepto);
    $("#checkboxporcentaje").on("change", function () { habilita_porcentaje_o_monto(); });

    $("#btnAbrirModalAgregarEmpleadoConcepto").click(modal_agregar_concepto);

    $("#TipoConcepto").on("change", function () { filtrar_tipo_concepto(); });
    $("#btnEliminarEmpleadoConcepto").on("click", function () { eliminar_empleado_concepto(); });

    $("#Concepto").on("change", function () { pago_fijo_variable(); });

    $("#Concepto").change(function () {
        var concepto = $(this).val();

        if (concepto === "CG" || concepto === "7") {
            var datos = {
                idPersona: $("#idPersona").val(),
                concepto: concepto
            };

            $.ajax({
                type: "POST",
                url: "/prestaciones/carga-compensacion-sueldo",
                data: JSON.stringify(datos),
                dataType: "json",
                contentType: "application/json; charset=utf-8",
                success: function (resultados) {
                    $('#Monto').val(resultados.Monto);
                    $('#Porcentaje').val(0);
                }
            });
        }
    });

    habilita_porcentaje_o_monto();

});

function funcionSeleccionar() { //se ejecuta al seleccionar el empleado en el modal
    buscar_empleado_concepto();
}

function filtrar_tipo_concepto(BuscarRepetidos) {
    $("#Concepto").val("0");
    datos = {}
    datos["TipoConcepto"] = $("#TipoConcepto").val();
    datos["idPersona"] = $("#idPersona").val();
    datos["BuscarRepetidos"] = BuscarRepetidos;
    datos["BuscarEditables"] = false;
    datos = JSON.stringify(datos);
    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/filtrar-conceptos",
        datatype: "json",
        contentType: "application/json; charset=utf-8",
        data: datos,
        success: function (resultados) {
            if (resultados.NoEncontrado) {
                console.log("ERROR empleado concepto");
            } else {
                $('#Concepto').empty();

                var nuevaOpcion = $('<option>', {
                    'value': "0",
                    'text': "-- Seleccione --"
                });
                $('#Concepto').append(nuevaOpcion);

                resultados.forEach(function (resultado) {
                    // Crea una nueva opción HTML
                    var nuevaOpcion = $('<option>', {
                        'value': resultado.idConcepto,
                        'text': resultado.Concepto + ' - ' + resultado.idConcepto
                    });

                    // Agrega la nueva opción al elemento select con id "Concepto"
                    $('#Concepto').append(nuevaOpcion);

                });
            }
        }
    });
}


function crear_empleado_concepto() {

    $("#TipoConcepto").prop('disabled', false);
    $("#Concepto").prop('disabled', false);

    if (validarFormulario($("#frmCrearConceptoEmpleado")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/prestaciones/crear-empleado-concepto",
            data: $("#frmCrearConceptoEmpleado, #idPersona").serialize(),
            success: function (data) {
                if (data.ContratoExistente) {
                    abrirModal("El concepto ya existe", "Verifique el numero de contrato", "");
                }

                else if (data.Existente) {
                    abrirModal("El concepto ya existe", "Ya existe un concepto con esas características", "");
                }
                else {
                    abrirModal("Información guardada", "Operación realizada con éxito", "");
                    buscar_empleado_concepto();
                    $('#ModalAgregaEmpleadoConcepto').modal('hide');
                }
            }
        });
    }
}

function buscar_empleado_concepto() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/buscar-empleado-concepto",
        data: $("#frmBuscarConceptoEmpleado, #idPersona").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
                $("#tablaResultadosEmpleadoConceptos tbody").empty();
                $("#tablaResultadosEmpleadoConceptos").hide();
                $("#btnAbrirModalAgregarEmpleadoConcepto").show();
            } else {
                $("#btnAbrirModalAgregarEmpleadoConcepto").show();
                $("#tablaResultadosEmpleadoConceptos").show();
                $("#tablaResultadosEmpleadoConceptosNoEditables").show();
                $("#tablaResultadosEmpleadoConceptos tbody").empty();
                $("#tablaResultadosEmpleadoConceptosNoEditables tbody").empty();
                var cont = 1;

                data.forEach(function (empleado_concepto) {
                    var text = ""; // Inicializa la variable text dentro del bucle
                    if (empleado_concepto.Editable == 1) {
                        console.log("Entro")
                        text += `
                                    <tr>
                                        <td>
                                            <div>
                                                <button type="button" class="btn btn-primary btn-sm" id="Editar_Aceptar${cont}" onclick="modal_editar_elemento(${cont})">
                                                    <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span>
                                                </button>
                                            </div>
                                        </td>
                                `;
                    } else {
                        text =  `<tr>
                                        <td>
                                        </td>
                                `;
                    }

                    text += `
                                <td>
                                    <input type="text" class="form-control" id="idTipoConcepto${cont}" value="${empleado_concepto.idTipoConcepto}" readonly>
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="idConcepto${cont}" value="${empleado_concepto.idConcepto}" readonly>
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="Concepto${cont}" value="${empleado_concepto.Concepto}" readonly style="width: 370px">
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="Porcentaje${cont}" value="${empleado_concepto.Porcentaje}" readonly>
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="Monto${cont}" value="${empleado_concepto.Monto}" readonly style="width: 120px">
                                </td>
                            `;

                    // Agregar más campos si es necesario
                    if (empleado_concepto.NumeroContrato != "1") {
                        var fechaInicial = empleado_concepto.FechaInicio ? convertirFechaParaVisualizacion(empleado_concepto.FechaInicio) : "";
                        var fechaFinal = empleado_concepto.FechaFin ? convertirFechaParaVisualizacion(empleado_concepto.FechaFin) : "";

                        text += `
            <td>
                <input type="hidden" class="form-control" id="NumeroContrato${cont}" value="${empleado_concepto.NumeroContrato}" readonly style="width: 100px">
                <input type="hidden" class="form-control" id="FechaInicio${cont}" value="${fechaInicial}" readonly style="width: 140px">
                <input type="hidden" class="form-control" id="FechaFin${cont}" value="${fechaFinal}" readonly style="width: 140px">
            </td>
        `;
                    }

                    text += `</tr>`; // Cierra la fila de la tabla

                    // Decide en qué tabla agregar la fila
                    if (empleado_concepto.Editable == 1) {
                        $("#tablaResultadosEmpleadoConceptos tbody").append(text);
                    } else {
                        $("#tablaResultadosEmpleadoConceptosNoEditables tbody").append(text);
                    }

                    cont++;
                });
            }
        }
    })

}
function pago_fijo_variable() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/obtener-concepto",
        data: $("#TipoConcepto, #Concepto").serialize(),
        success: function (respuesta) {

            if (respuesta.NoEncontrado == true) {
                abrirModal("ERROR", "Error", "");
            } else {
                if (respuesta.concepto.idTipoPago == "2") {//Si es == 2 (Variable)
                    $("#contenedorCheckbox").show();
                    $("#Monto").val("0.00");
                    $("#Porcentaje").val("0.000");
                    $("#Monto").prop('readonly', false);
                    $("#Porcentaje").prop('readonly', false);
                    habilita_porcentaje_o_monto();
                } else {
                    $("#contenedorCheckbox").hide();

                    $("#Monto").val(respuesta.concepto.Monto);
                    $("#Porcentaje").val(respuesta.concepto.Porcentaje);

                    $("#Monto").prop('readonly', true);
                    $("#Porcentaje").prop('readonly', true);
                }

                if (respuesta.concepto.Contrato == "1") {
                    $("#NumeroContrato").addClass("obligatorio");
                    $("#FechaInicioContrato").addClass("obligatorio");
                    $("#FechaFinContrato").addClass("obligatorio");

                    $("#NumeroContrato").prop('disabled', false)
                    $("#FechaInicioContrato").prop('disabled', false)
                    $("#FechaFinContrato").prop('disabled', false)
                    $("#ContenedorContrato").show();

                }
                else {
                    $("#NumeroContrato").removeClass("obligatorio");
                    $("#FechaInicioContrato").removeClass("obligatorio");
                    $("#FechaFinContrato").removeClass("obligatorio");


                    $("#NumeroContrato").prop('disabled', true)
                    $("#FechaInicioContrato").prop('disabled', true)
                    $("#FechaFinContrato").prop('disabled', true)
                    $("#ContenedorContrato").hide();

                }

            }
        }
    });


}

function habilita_porcentaje_o_monto() {
    if ($("#checkboxporcentaje").prop("checked")) {

        $("#Monto").prop('readonly', true);
        $("#Monto").val("0.00")
        $("#Monto").removeClass("obligatorio");
        $("#Porcentaje").addClass("obligatorio");
        $("#Porcentaje").prop('readonly', false);
        $("#Porcentaje").val("0.000")

    } else {
        $("#Monto").prop('readonly', false);
        $("#Monto").val("0.00")

        $("#Porcentaje").prop('readonly', true);
        $("#Porcentaje").val("0.000")
    }

}

function modal_agregar_concepto() {
    $('#ModalAgregaEmpleadoConcepto').modal('show');
    $("#btnEliminarEmpleadoConcepto").hide();
    $("#consecutivo").val("");
    $("#TipoConcepto").prop('disabled', false);

    $("#Concepto").empty();
    $("#Concepto").append("<option value='0'>-- Seleccione --</option>");
    $("#Concepto").prop('disabled', false);

    $('#tituloModalAgregaEmpleadoConcepto')[0].textContent = "Agregar concepto";
    $('#btnCrearEmpleadoConcepto')[0].textContent = "Agregar";
    $("#Concepto").val("0");
    $("#TipoConcepto").val("0");
    $("#Monto").val("0.00");
    $("#Porcentaje").val("0.000");
    $("#editar").val(false);

    $("#NumeroContrato").val("");
    $("#FechaInicioContrato").val("");
    $("#FechaFinContrato").val("");

    $("#ContenedorContrato").hide();


}



function modal_editar_elemento(consecutivo) {

    $('#ModalAgregaEmpleadoConcepto').modal('show');
    $("#consecutivo").val(consecutivo);
    $("#btnEliminarEmpleadoConcepto").show();
    $('#tituloModalAgregaEmpleadoConcepto')[0].textContent = "Modificar concepto asignado";
    $('#btnCrearEmpleadoConcepto')[0].textContent = "Modificar";
    $("#editar").val(true);
    $("#TipoConcepto").val($("#idTipoConcepto" + consecutivo).val());

    filtrar_tipo_concepto("true");

    $("#Concepto").val($("#idConcepto" + consecutivo).val());
    $("#Monto").val($("#Monto" + consecutivo).val());
    $("#Porcentaje").val($("#Porcentaje" + consecutivo).val());

    $("#NumeroContrato").val($("#NumeroContrato" + consecutivo).val());
    $("#FechaInicioContrato").val($("#FechaInicio" + consecutivo).val());
    $("#FechaFinContrato").val($("#FechaFin" + consecutivo).val());

    $("#TipoConcepto").prop('disabled', true);
    $("#Concepto").prop('disabled', true);

    if ($("#NumeroContrato" + consecutivo).val() !== undefined) {

        if ($("#NumeroContrato" + consecutivo).val() == "1") {

            $("#ContenedorContrato").hide();
        } else {
            $("#ContenedorContrato").show();
        }

    } else {
        $("#ContenedorContrato").hide();
    }
}

function eliminar_empleado_concepto() {

    $("#TipoConcepto").prop('disabled', false);
    $("#Concepto").prop('disabled', false);

    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/eliminar-empleado-concepto",
        data: $("#frmCrearConceptoEmpleado, #idPersona").serialize(),
        success: function (data) {
            if (data.eliminado) {
                abrirModal("Relación eliminada", "Operación realizada con éxito", "");
                buscar_empleado_concepto();
                $('#ModalAgregaEmpleadoConcepto').modal('hide');
            }
        }
    });

}