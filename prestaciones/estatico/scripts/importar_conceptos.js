$gmx(document).ready(function () {


    cargar_conceptos_extraeArchivo();

});

function cargar_conceptos_extraeArchivo() {

    $.ajax({
        async: false,
        type: "POST",
        url: "/prestaciones/filtrar-conceptos-extrae-archivo",
        // data: $("#frmBuscarConceptoEmpleado, #idPersona").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.", "")
                $("#tablaResultadosConceptos tbody").empty();
                $("#tablaResultadosConceptos").hide();
            } else {
                $("#tablaResultadosConceptos").show();
                $("#tablaResultadosConceptos tbody").empty();
                var cont = 1;
                data.forEach(function (concepto) {
                    text = `
                    <tr>
                        <td>
                            <input type="text" class="form-control" id="idTipoConcepto${cont}" value="${concepto.idTipoConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="idConcepto${cont}" value="${concepto.idConcepto}" readonly></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Concepto${cont}" value="${concepto.Concepto}" readonly style="width: 370px"></input>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Abreviatura${cont}" value="${concepto.Abreviatura}" readonly></input>
                        </td>
                        
                        <td>
                            <input type="text" class="form-control" id="ClaveSAT${cont}" value="${concepto.ClaveSAT}" readonly style="width: 120px"></input>
                        </td>
                        
                        `;


                    text = text + `
                        <td>
                        <div>
                            <button type="button" class="btn btn-primary btn-sm" id="Editar_Aceptar${cont}" onclick="modal_editar_elemento(${cont})"> <span class="glyphicon glyphicon-pencil" aria-hidden="true"></span> </button>
                        </div>
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