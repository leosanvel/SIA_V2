$gmx(document).ready(function () {
    $("#btnBuscaEmpleadoConcepto").click(buscar_empleado_concepto);
    $("#btnCrearEmpleadoConcepto").click(crear_empleado_concepto);
    $("#checkboxporcentaje").on("change", function () { habilita_porcentaje_o_monto(); });

    $("#btnAgregarEmpleadoConcepto").click(modal_agregar_concepto);

    $("#TipoConcepto").change(filtrar_tipo_concepto);
    $("#Concepto").change(pago_fijo_variable);

    habilita_porcentaje_o_monto();

});
function filtrar_tipo_concepto() {
    $("#Concepto").val("0");
    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/filtrar-conceptos",
        data: $("#TipoConcepto, #idPersona").serialize(),
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
    console.log("Boton");
    if (validarFormulario($("#frmCrearConceptoEmpleado")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/prestaciones/crear-empleado-concepto",
            data: $("#frmCrearConceptoEmpleado, #idPersona").serialize(),
            success: function (data) {
                if (data) {
                    console.log("CREADO");
                    abrirModal("Información guardada", "El concepto se creó con éxito", "");
                    buscar_empleado_concepto();
                }
            }
        });
    }
}

function buscar_empleado_concepto() {
    console.log("BUSCAR");
    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/buscar-empleado-concepto",
        data: $("#frmBuscarConceptoEmpleado, #idPersona").serialize(),
        success: function (data) {
            console.log("Peticion completa!")
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
                $("#btnAgregarEmpleadoConcepto").show();
            } else {
                $("#btnAgregarEmpleadoConcepto").show();
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
                            <input type="text" class="form-control" id="Porcentaje${cont}" value="${empleado_concepto.Porcentaje}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Monto${cont}" value="${empleado_concepto.Monto}" readonly></input>
                        </td>

                        <td>
                        </td>
                        <td>
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
            }else{
                if (concepto.idTipoPago == "2") {//Si es == 2 (Variable)
                    $("#contenedorCheckbox").show();
                    $("#Monto").val("0.00");
                    $("#Porcentaje").val("0.000");
                    $("#Monto").prop('readonly', false);
                    $("#Porcentaje").prop('readonly', false);
                    habilita_porcentaje_o_monto();
                }else{
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
    console.log("MODAL!!")
    $('#ModalAgregaEmpleadoConcepto').modal('show');
}