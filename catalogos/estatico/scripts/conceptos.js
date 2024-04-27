$gmx(document).ready(function () {
    $("#btnBuscaConcepto").click(buscar_concepto);
    $("#btnCrearConcepto").click(crear_concepto);
    $("#TipoPago").change(function () { pago_fijo_variable($(this).val()); });

    $("#MontoContenedor").hide();
    $("#PorcentajeContenedor").hide();
    $("#contenedorCheckbox").hide();

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


});


function actualizarListaDesplegable(resultados) {
    var listaDesplegable = $('#lista_conceptos');
    listaDesplegable.empty(); // Vaciar la lista desplegable antes de agregar nuevos elementos
    resultados.forEach(function (resultado) {
        var nuevoElemento = $('<div>', {
            'class': 'dropdown-item form-group',
            'html': $('<a>', {
                'href': 'javascript:void(0)', // El href está configurado para evitar que la página se recargue
                'data-id': resultado.idConcepto,
                'data-texto': resultado.texto,
                'text': resultado.texto,
                'click': function () {
                    var textoSeleccionado = $(this).data('texto');
                    $('#ConceptoExistente').val(textoSeleccionado);
                    $('#lista_conceptos').hide();
                }
            })
        });
        listaDesplegable.append(nuevoElemento);
    });


}




function crear_concepto() {
    console.log("Boton");
    if (validarFormulario($("#frmCrearConcepto")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/crear-concepto",
            data: $("#frmCrearConcepto").serialize(),
            success: function (data) {
                if (data) {
                    console.log("CREADO");
                    abrirModal("Información guardada", "El concepto se creó con éxito", "recargar");
                }
            }
        });
    }
}

function buscar_concepto() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/buscar-concepto",
        data: $("#frmBuscarConcepto").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
            } else {
                $("#tablaResultadosConceptos").show();
                $("#tablaResultadosConceptos tbody").empty();
                var cont = 1;
                data.forEach(function (concepto) {
                    text = `
                    <tr>
                        
                        <td>
                            <input type="text" class="form-control" id="TipoConcepto" value="${concepto.idTipoConcepto}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto" value="${concepto.idConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto" value="${concepto.Concepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Abreviatura" value="${concepto.Abreviatura}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Porcentaje" value="${concepto.Porcentaje}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Monto" value="${concepto.Monto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="ClaveSAT" value="${concepto.ClaveSAT}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idTipoPago" value="${concepto.idTipoPago}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Activo" value="${concepto.Activo}" readonly></input>
                        </td>

                        <td>
                        </td>
                        <td>
                        </td>


                    </tr>
                    `;
                    cont++;
                    $("#tablaResultadosConceptos tbody").append(text);
                });
            }
        }
    })

}

function habilita_porcentaje_o_monto() {
    if ($("#checkboxporcentaje").prop("checked")) {

        $("#Monto").prop('disabled', true);
        $("#Porcentaje").prop('disabled', false);
        $("#Monto").val("0.00")
        $("#Monto").addClass("obligatorio");
        $("#Porcentaje").removeClass("obligatorio");
    } else {
        $("#Porcentaje").prop('disabled', true);
        $("#Monto").prop('disabled', false);
        $("#Porcentaje").val("0.000")
        $("#Porcentaje").addClass("obligatorio");
        $("#Monto").removeClass("obligatorio");
    }

}

function pago_fijo_variable(TipoPago) {
    if (TipoPago == "2") {//Si es == 2 (Variable)
        $("#Monto").removeClass("obligatorio");
        $("#Porcentaje").removeClass("obligatorio");
        $("#Monto").val("0.00")
        $("#Porcentaje").val("0.000")
        $("#Porcentaje").prop('disabled', false);
        $("#Monto").prop('disabled', false);
        $("#MontoContenedor").hide();
        $("#PorcentajeContenedor").hide();
        $("#contenedorCheckbox").hide();

    } else {
        $("#Monto").val("0.00")
        $("#Porcentaje").val("0.000")
        $("#MontoContenedor").show();
        $("#PorcentajeContenedor").show();
        $("#contenedorCheckbox").show();
        habilita_porcentaje_o_monto();
    }

}