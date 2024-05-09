$gmx(document).ready(function () {
    $("#btnBuscaEmpleadoConcepto").click(buscar_empleado_concepto);
    $("#btnCrearEmpleadoConcepto").click(crear_empleado_concepto);
    $("#checkboxporcentaje").on("change", function () { habilita_porcentaje_o_monto(); });

    $("#btnAbrirModalAgregarEmpleadoConcepto").click(modal_agregar_concepto);

    $("#TipoConcepto").on("change", function () { filtrar_tipo_concepto("false"); });
    $("#btnEliminarEmpleadoConcepto").on("click", function () { eliminar_empleado_concepto(); });
    $("#Concepto").change(pago_fijo_variable);

    habilita_porcentaje_o_monto();

});

function funcionSeleccionar() { //se ejecuta al seleccionar el empleado
    buscar_empleado_concepto();
}

function filtrar_tipo_concepto(BuscarRepetidos) {
    $("#Concepto").val("0");
    datos = {}
    datos["TipoConcepto"] = $("#TipoConcepto").val();
    datos["idPersona"] = $("#idPersona").val();
    datos["BuscarRepetidos"] = BuscarRepetidos;
    datos = JSON.stringify(datos);
    $.ajax({
        async:false,
        type: "POST",
        url: "/prestaciones/filtrar-conceptos",
        datatype: "json",
        contentType: "application/json; charset=utf-8",
        data: datos,
        success: function (resultados) {
            if (resultados.NoEncontrado) {
                console.log("ERROR empleado concepto");
            } else {

                resultados.forEach(function (resultado) {
                    // Crea una nueva opción HTML
                    var nuevaOpcion = $('<option>', {
                        'value': resultado.idConcepto,
                        'text': resultado.idConcepto + ' - ' + resultado.Concepto
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
                if (data) {
                    abrirModal("Información guardada", "Operación realizada con éxito", "");
                    buscar_empleado_concepto();
                    $('#ModalAgregaEmpleadoConcepto').modal('hide');
                }
            }
        });
    }
}

function buscar_empleado_concepto() {
    console.log("BUSCANDO");
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
                $("#tablaResultadosEmpleadoConceptos tbody").empty();
                var cont = 1;
                data.forEach(function (empleado_concepto) {
                    text = `
                    <tr>
                        
                        <td>
                            <input type="text" class="form-control" id="NumeroEmpleado${cont}" value="${empleado_concepto.NumeroEmpleado}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idTipoConcepto${cont}" value="${empleado_concepto.idTipoConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto${cont}" value="${empleado_concepto.idConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto${cont}" value="${empleado_concepto.Concepto}" readonly style="width: 500px"></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Porcentaje${cont}" value="${empleado_concepto.Porcentaje}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Monto${cont}" value="${empleado_concepto.Monto}" readonly style="width: 140px"></input>
                        </td>

                        <td>
                        <div>
                            <button type="button" class="btn btn-primary btn-sm" id="Editar_Aceptar${cont}" onclick="modal_editar_elemento(${cont})"> <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span> </button>
                        </div>
                        </td>
                    </tr>
                    `;
                    cont++;
                    $("#tablaResultadosEmpleadoConceptos tbody").append(text);
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
        success: function (concepto) {
            if (concepto.NoEncontrado) {
                abrirModal("ERROR", "Error", "");
            } else {
                if (concepto.idTipoPago == "2") {//Si es == 2 (Variable)
                    $("#contenedorCheckbox").show();
                    $("#Monto").val("0.00");
                    $("#Porcentaje").val("0.000");
                    $("#Monto").prop('readonly', false);
                    $("#Porcentaje").prop('readonly', false);
                    habilita_porcentaje_o_monto();
                } else {
                    $("#contenedorCheckbox").hide();

                    $("#Monto").val(concepto.Monto);
                    $("#Porcentaje").val(concepto.Porcentaje);

                    $("#Monto").prop('readonly', true);
                    $("#Porcentaje").prop('readonly', true);
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
}



function modal_editar_elemento(consecutivo) {

    $('#ModalAgregaEmpleadoConcepto').modal('show');
    $("#consecutivo").val(consecutivo);
    $("#btnEliminarEmpleadoConcepto").show();
    $('#tituloModalAgregaEmpleadoConcepto')[0].textContent = "Modificar concepto asignado";
    $('#btnCrearEmpleadoConcepto')[0].textContent = "Modificar";

    $("#TipoConcepto").val($("#idTipoConcepto" + consecutivo).val());

    filtrar_tipo_concepto("true");

    $("#Concepto").val($("#idConcepto" + consecutivo).val());
    $("#Monto").val($("#Monto" + consecutivo).val());
    $("#Porcentaje").val($("#Porcentaje" + consecutivo).val());

    $("#TipoConcepto").prop('disabled', true);
    $("#Concepto").prop('disabled', true);

    // pago_fijo_variable();
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