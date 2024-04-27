$gmx(document).ready(function () {
    $("#btnBuscaEmpleadoConcepto").click(buscar_empleado_concepto);
    $("#btnCrearEmpleadoConcepto").click(crear_empleado_concepto);
    $("#checkboxporcentaje").on("change", function () { habilita_porcentaje_o_monto(); });

    $('#ConceptoExistente').on('focus', function () {
        $('#lista_conceptos').show();
    });

    $('#ConceptoExistente').on('blur', function (event) {
        if (!$(event.relatedTarget).closest('#lista_conceptos').length) {
            $('#lista_conceptos').hide();
        }
    });

    $('#ConceptoExistente').on('input', function () {
        var textoBusqueda = $(this).val();
        $.ajax({
            url: '/catalogos/actualizar-busqueda-conceptos',
            method: 'GET',
            data: { texto_busqueda: textoBusqueda },
            success: function (response) {
                actualizarListaDesplegable(response);

            }
        });
    });
    habilita_porcentaje_o_monto();

});

function actualizarListaDesplegable(resultados) {
    var listaDesplegable = $('#lista_conceptos');
    listaDesplegable.empty(); // Vaciar la lista desplegable antes de agregar nuevos elementos
    resultados.forEach(function (resultado) {
        var nuevoElemento = $('<div>', {
            'class': 'dropdown-item form-group',
            'html': $('<a>', {
                'href': 'javascript:void(0)', // El href está configurado para evitar que la página se recargue
                'text': resultado.texto,
                'click': function () {

                    $('#ConceptoExistente').val(resultado.texto);
                    $('#lista_conceptos').hide();

                    pago_fijo_variable(resultado.idTipoPago, resultado.Monto, resultado.Porcentaje);


                }
            })
        });
        listaDesplegable.append(nuevoElemento);
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
                    abrirModal("Información guardada", "El concepto se creó con éxito", "recargar");
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
            } else {
                $("#tablaResultadosEmpleadoConceptos").show();
                $("#tablaResultadosEmpleadoConceptos tbody").empty();
                var cont = 1;
                data.forEach(function (empleado_concepto) {
                    text = `
                    <tr>
                        
                        <td>
                            <input type="text" class="form-control" id="TipoConcepto" value="${empleado_concepto.NoEmpleado}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto" value="${empleado_concepto.idTipoConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto" value="${empleado_concepto.idConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Abreviatura" value="${empleado_concepto.Porcentaje}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Porcentaje" value="${empleado_concepto.Monto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Activo" value="${empleado_concepto.Activo}" readonly></input>
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
function pago_fijo_variable(TipoPago, Monto, Porcentaje) {
    console.log("TipoPagoAAA");
    console.log(TipoPago);
    if (TipoPago == "2") {//Si es == 2 (Variable)

        $("#Monto").val("0.00")
        $("#Porcentaje").val("0.000")
        $("#MontoContenedor").show();
        $("#PorcentajeContenedor").show();
        $("#contenedorCheckbox").show();
        habilita_porcentaje_o_monto();

    } else {
        $("#Monto").removeClass("obligatorio");
        $("#Porcentaje").removeClass("obligatorio");
        $("#Porcentaje").prop('disabled', false);
        $("#Monto").prop('disabled', false);
        if (Monto) {
            console.log("IF MONTO")
            $("#Monto").val(Monto);
        }else{
            console.log("ELSE MONTO")
            $("#Monto").val(0);
        }
        $("#Porcentaje").val(Porcentaje);
        $("#MontoContenedor").hide();
        $("#PorcentajeContenedor").hide();
        $("#contenedorCheckbox").hide();
    }

}

function habilita_porcentaje_o_monto() {
    if ($("#checkboxporcentaje").prop("checked")) {

        $("#Monto").prop('disabled', true);
        $("#Monto").val("0.00")
        $("#Monto").removeClass("obligatorio");
        $("#Porcentaje").addClass("obligatorio");
        $("#Porcentaje").prop('disabled', false);
        $("#Porcentaje").val("0.000")

    } else {
        $("#Monto").prop('disabled', false);
        $("#Monto").val("0.00")

        $("#Porcentaje").prop('disabled', true);
        $("#Porcentaje").val("0.000")
    }

}