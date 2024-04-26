$gmx(document).ready(function () {
    $("#btnBuscaEmpleadoConcepto").click(buscar_empleado_concepto);
    $("#btnCrearEmpleadoConcepto").click(crear_empleado_concepto);
});

function crear_empleado_concepto() {
    console.log("Boton");
    if (validarFormulario($("#frmCrearConceptoEmpleado")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/crear-empleado-concepto",
            data: $("#frmCrearConceptoEmpleado").serialize(),
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
        url: "/buscar-empleado-concepto",
        data: $("#frmBuscarConceptoEmpleado").serialize(),
        success: function (data) {
            if (data.NoEncontrado) {
                abrirModal("No encontrado", "No se encontraron coincidencias.","")
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