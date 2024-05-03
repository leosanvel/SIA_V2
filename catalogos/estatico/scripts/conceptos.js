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
        success: function (respuesta) {
            if (respuesta.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
            } else {
                $("#tablaResultadosConceptos").show();
                $("#tablaResultadosConceptos tbody").empty();
                var cont = 1;
                
                opcionHTML = `<option value="0">-- Seleccione --</option>`
                respuesta.TipoPago.forEach(function (tipoPago) {
                    opcionHTML += `<option value='${tipoPago.idTipoPago}'> ${tipoPago.TipoPago} </option>`;
                });
                console.log("opcionHTML")
                console.log(opcionHTML)

                respuesta.ListaConceptos.forEach(function (concepto) {
                    text = `
                    <tr>  
                        <td>
                            <input type="text" class="form-control" id="TipoConcepto${cont}" value="${concepto.idTipoConcepto}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto${cont}" value="${concepto.idConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto${cont}" value="${concepto.Concepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Abreviatura${cont}" value="${concepto.Abreviatura}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Porcentaje${cont}" value="${concepto.Porcentaje}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Monto${cont}" value="${concepto.Monto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="ClaveSAT${cont}" value="${concepto.ClaveSAT}" readonly></input>
                        </td>
                        <td>
                            <select id="TipoPago${cont}" name="TipoPago${cont}" class="obligatorio form-control">
                            </select>
                        </div>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Activo${cont}" value="${concepto.Activo}" readonly></input>
                        </td>

                        <td>
                            <div style="display: block;">
                            <button type="button" class="btn btn-primary" id="Editar_Aceptar${cont}" onclick="editar_aceptar(${cont})">Editar</button>
                        </div>
                        </td>
                        <td>
                            <div style="display: block;">
                                <button type="button" class="btn btn-secondary" id="Cancelar${cont}" onclick="cancelar('${cont}')" style="display: none">Cancelar</button>
                            </div>
                        </td>


                    </tr>
                    `;
                    $("#tablaResultadosConceptos tbody").append(text);
                    $("#TipoPago" + cont).html(opcionHTML);
                    $("#TipoPago" + cont).val(concepto.idTipoPago);
                    $("#TipoPago" + cont).prop('disabled', true);
                    cont++;
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

function editar_aceptar(data) {
    if ($("#Editar_Aceptar" + data).text() == "Editar") {
        
        $("#Porcentaje" + data).attr("readonly", false);
        $("#Monto" + data).attr("readonly", false);
        $("#ClaveSAT" + data).attr("readonly", false);
        $("#TipoPago" + data).attr("disabled", false);
        $("#Activo" + data).attr("readonly", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else {
        guardar_modificar_porcentaje(data);
    }
}

function cancelar(data) {

    $("#Porcentaje" + data).attr("readonly", true);
    $("#Monto" + data).attr("readonly", true);
    $("#ClaveSAT" + data).attr("readonly", true);
    $("#TipoPago" + data).attr("disabled", true);
    $("#Activo" + data).attr("readonly", true);
    
    $("#Editar_Aceptar" + data).text("Editar");
    $("#Cancelar" + data).toggle();
}

function guardar_modificar_porcentaje(dato) {
    datos = {}
    if (dato) {
        datos["idPorcentaje"] = dato;
        datos["Porcentaje"] = $("#porcentaje" + dato).val();
        datos["Activo"] = $("#Activo" + dato).val();
        var valido = ($("#porcentaje" + dato).val()) ? true : false;
        datos = JSON.stringify(datos);
    }
    else {
        datos["Porcentaje"] = $("#porcentaje").val();
        console.log(datos["Porcentaje"])
        datos["Activo"] = $("#Activo").val() - 1;
        datos = JSON.stringify(datos);
        valido = validarFormulario($("#formularioPorcentajes")).valido
    }

    if (valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/Catalogos/guardar_porcentajes",
            datatype: "json",
            contentType: "application/json; charset=utf-8",
            data: datos,
            success: function (data) {
                if (data.guardado) {
                    abrirModal("Información guardada", "Los datos de Tipo de Justificante se guardaron correctamente.", "recargar");
                }
            }
        })
    }
}