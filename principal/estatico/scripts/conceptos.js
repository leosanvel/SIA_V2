$gmx(document).ready(function () {
    $("#btnBuscaConcepto").click(buscar_concepto);
    $("#btnCrearConcepto").click(crear_concepto);
});

function crear_concepto() {
    console.log("Boton");
    if (validarFormulario($("#frmCrearConcepto")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/crear-concepto",
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
    console.log("BUSCAR");
    $.ajax({
        async: false,
        type: "POST",
        url: "/buscar-concepto",
        data: $("#frmBuscarConcepto").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.","")
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