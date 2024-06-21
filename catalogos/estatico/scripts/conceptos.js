$gmx(document).ready(function () {

    $("#btnAbrirModalCrearConcepto").click(modal_crear_concepto);

    $("#btnBuscaConcepto").click(buscar_concepto);
    $("#btnCrearConcepto").click(crear_concepto);

    $("#TipoPago").change(function () { pago_fijo_variable($(this).val()); });

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

function modal_crear_concepto() {
    $('#ModalCrearConcepto').modal('show');
    $("#Estatus").val("2");
    $("#ContenedorEstatus").hide();

    $("#consecutivo").val("");

    $("#TipoConcepto").prop('disabled', false);
    $("#TipoEmpleado").prop('disabled', false);
    $("#idConcepto").prop('readonly', false);
    $("#Concepto").prop('readonly', false);
    $("#Abreviatura").prop('readonly', false);
    $("#ClaveSAT").prop('readonly', false);
    $("#TipoPago").prop('disabled', false);

    $('#tituloModalCrearConcepto')[0].textContent = "Crear nuevo concepto";
    $('#btnCrearConcepto')[0].textContent = "Crear";

    $("#TipoConcepto").val("0");
    $("#TipoEmpleado").val("0");
    $("#idConcepto").val("");
    $("#Concepto").val("");
    $("#Abreviatura").val("");
    $("#Partida").val("");
    $("#ClaveSAT").val("");
    $("#TipoPago").val("0");
    $("#Monto").val("0.00");
    $("#Porcentaje").val("0.000");
    $("#checkboxporcentaje").prop('checked', true);
    $("#checkboxContrato").prop('checked', false);
    $("#checkboxImportacion").prop('checked', false);
    $("#checkboxEditable").prop('checked', false);
    habilita_porcentaje_o_monto();
}

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
    $("#TipoConcepto").prop('disabled', false);
    $("#TipoEmpleado").prop('disabled', false);
    $("#TipoPago").prop('disabled', false);
    console.log($("#checkboxImportacion").prop('checked'))
    if (validarFormulario($("#frmCrearConcepto")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/crear-concepto",
            data: $("#frmCrearConcepto").serialize(),
            success: function (data) {
                if (data) {
                    abrirModal("Información guardada", "Operación realizada con éxito", "");
                    $('#ModalCrearConcepto').modal('hide');
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


                respuesta.ListaConceptos.forEach(function (concepto) {
                    text = `
                    <tr>  
                    <input type="hidden" id="Contrato${cont}" value="${concepto.Contrato}"></input>
                    <input type="hidden" class="form-control" id="Abreviatura${cont}" value="${concepto.Abreviatura}" readonly></input>
                    <input type="hidden" class="form-control" id="Porcentaje${cont}" value="${concepto.Porcentaje}" readonly></input>
                    <input type="hidden" class="form-control" id="Monto${cont}" value="${concepto.Monto}" readonly></input>
                    <input type="hidden" class="form-control" id="ClaveSAT${cont}" value="${concepto.ClaveSAT}" readonly></input>
                    <input type="hidden" class="form-control" id="TipoPago${cont}" value="${concepto.idTipoPago}" readonly style="width: 100;"></input>
                    <input type="hidden" class="form-control" id="Contrato${cont}" value="${concepto.Contrato}" readonly></input>
                    <input type="hidden" class="form-control" id="Importacion${cont}" value="${concepto.ExtraeArchivo}" readonly></input>
                    <input type="hidden" class="form-control" id="Editable${cont}" value="${concepto.Editable}" readonly></input>

                    
                        <td>
                            <input type="text" class="form-control" id="TipoConcepto${cont}" value="${concepto.idTipoConcepto}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="TipoEmpleado${cont}" value="${concepto.idTipoEmpleado}" readonly></input></td>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto${cont}" value="${concepto.idConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto${cont}" value="${concepto.Concepto}" readonly style="width: 400px;"></input>
                        </td>
                        
                        <td>
                            <input type="text" class="form-control" id="Partida${cont}" value="${concepto.Partida}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Activo${cont}" value="${concepto.Activo}" readonly></input>
                        </td>
                     
                        <td>
                            <div style="display: block;">
                                <button type="button" class="btn btn-primary btn-sm" id="Editar_Aceptar${cont}" onclick="editar_concepto(${cont})"><span class="glyphicon glyphicon-pencil" aria-hidden="true"></span></button>
                            </div>
                        </td>


                    </tr>
                    `;
                    $("#tablaResultadosConceptos tbody").append(text);
                    cont++;
                });
            }
        }
    })

}

function habilita_porcentaje_o_monto() {
    if ($("#checkboxporcentaje").prop("checked")) {

        $("#Monto").prop('readonly', true);
        $("#Porcentaje").prop('readonly', false);
        $("#Monto").val("0.00")
        $("#Monto").addClass("obligatorio");
        $("#Porcentaje").removeClass("obligatorio");
    } else {
        $("#Porcentaje").prop('readonly', true);
        $("#Monto").prop('readonly', false);
        $("#Porcentaje").val("0.000")
        $("#Porcentaje").addClass("obligatorio");
        $("#Monto").removeClass("obligatorio");
    }

}

function pago_fijo_variable(TipoPago) {
    console.log("FUNCION PAGO FIJO O VARIABLE");
    if (TipoPago == "2") {//Si es == 2 (Variable)
        console.log("TIPO 2 VARIABLE");
        $("#Monto").val("0.00")
        $("#Porcentaje").val("0.000")
        $("#Porcentaje").prop('readonly', true);
        $("#Monto").prop('readonly', true);
        $("#contenedorCheckbox").hide();

    } else {
        console.log("TIPO 1 FIJO");
        $("#Monto").val("0.00")
        $("#Porcentaje").val("0.000")
        $("#Porcentaje").prop('readonly', false);
        $("#Monto").prop('readonly', false);
        $("#contenedorCheckbox").show();
        habilita_porcentaje_o_monto();
    }

}

function editar_concepto(consecutivo) {

    $('#ModalCrearConcepto').modal('show');

    $("#consecutivo").val(consecutivo);

    $("#TipoConcepto").prop('disabled', true);
    $("#idConcepto").prop('readonly', true);
    $("#Concepto").prop('readonly', true);
    $("#Abreviatura").prop('readonly', true);
    $("#ClaveSAT").prop('readonly', true);
    $("#TipoPago").prop('disabled', false);
    
    $("#TipoEmpleado").prop('disabled', true);
    $("#TipoEmpleado").val($("#TipoEmpleado" + consecutivo).val());

    console.log( '$("#TipoConcepto")')
    console.log( $("#TipoConcepto"))
    console.log( '$("#TipoEmpleado")')
    console.log( $("#TipoEmpleado"))

    $('#tituloModalCrearConcepto')[0].textContent = "Editar concepto";
    $('#btnCrearConcepto')[0].textContent = "Editar";

    $("#TipoConcepto").val($("#TipoConcepto" + consecutivo).val());
    $("#idConcepto").val($("#idConcepto" + consecutivo).val());
    $("#Concepto").val($("#Concepto" + consecutivo).val());
    $("#Abreviatura").val($("#Abreviatura" + consecutivo).val());
    $("#ClaveSAT").val($("#ClaveSAT" + consecutivo).val());
    $("#TipoPago").val($("#TipoPago" + consecutivo).val());
    

    $("#Partida").val(parseInt($("#Partida" + consecutivo).val()));
    $("#checkboxImportacion").prop("checked", $("#Importacion" + consecutivo).val() === '1');
    $("#checkboxContrato").prop("checked", $("#Contrato" + consecutivo).val() === '1');
    $("#checkboxEditable").prop("checked", $("#Editable" + consecutivo).val() === '1');

    if ($("#TipoPago").val() == "2") {//Si es == 2 (Variable)

        $("#Monto").val("0.00")
        $("#Porcentaje").val("0.000")
        $("#Porcentaje").prop('readonly', true);
        $("#Monto").prop('readonly', true);
        $("#contenedorCheckbox").hide();

    } else {
        $("#Monto").val($("#Monto" + consecutivo).val());
        $("#Porcentaje").val($("#Porcentaje" + consecutivo).val());

        $("#Porcentaje").prop('readonly', false);
        $("#Monto").prop('readonly', false);
        $("#contenedorCheckbox").show();
        habilita_porcentaje_o_monto();
    }

    $("#ContenedorEstatus").show();
    $("#Estatus").val(parseInt($("#Activo" + consecutivo).val()) + 1);
}

function cancelar(consecutivo) {

    $("#Porcentaje" + consecutivo).attr("readonly", true);
    $("#Monto" + consecutivo).attr("readonly", true);
    $("#ClaveSAT" + consecutivo).attr("readonly", true);
    $("#TipoPago" + consecutivo).attr("disabled", true);
    $("#Activo" + consecutivo).attr("readonly", true);

    $("#Editar_Aceptar" + consecutivo).text("Editar");
    $("#Cancelar" + consecutivo).toggle();
}

function guardar_modificar_porcentaje(consecut) {
    datos = {}
    if (consecut) {
        datos["idPorcentaje"] = consecut;
        datos["Porcentaje"] = $("#porcentaje" + consecut).val();
        datos["Activo"] = $("#Activo" + consecut).val();
        var valido = ($("#porcentaje" + consecut).val()) ? true : false;
        datos = JSON.stringify(datos);
    }
    else {
        datos["Porcentaje"] = $("#porcentaje").val();
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