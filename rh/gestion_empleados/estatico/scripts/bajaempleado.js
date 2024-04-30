$gmx(document).ready(function () {

    $("#btnBuscaBajaEmpleado").click(function (event) {
        var idPersona = $("#idPersona").val()
        if (idPersona) {
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-empleados/obtener-puestos-empleado",
                data: {
                    "idPersona": $("#idPersona").val()
                },
                success: function (lista_puestos) {
                    if (lista_puestos.length) {
                        var cont = 1;
                        $("#tablaResultadosEmpleadoPuestos tbody").empty();
                        $("#tablaResultadosEmpleadoPuestos").show();
                        lista_puestos.forEach(function (puesto) {
                            var FechaInicio = convertirFechaParaVisualizacion(puesto.FechaInicio);
                            var FechaFin = convertirFechaParaVisualizacion(puesto.FechaTermino);
                            var text = `
                            <tr>
                                <td><input type="text" class="form-control" id="idPersona${cont}" value=${puesto.idPersona} data-chbxvalue="${cont}" readonly"></td>
                                <td><input type="text" class="form-control" id="idPuesto${cont}" value=${puesto.idPuesto} data-chbxvalue="${cont}" readonly></td>
                                <td><input type="text" class="form-control" id="FechaInicio${cont}" value="${FechaInicio}" data-chbxvalue="${cont}" readonly></td>
                                <td><input type="text" class="form-control" id="FechaFin${cont}" value="${FechaFin}" data-chbxvalue="${cont}" readonly></td>
                                <td><input type="text" class="form-control" id="Activo${cont}" value=${puesto.idEstatusEP} data-chbxvalue="${cont}" readonly></td>
                            </tr>
                            
                            `;
                            cont++;
                            $("#tablaResultadosEmpleadoPuestos tbody").append(text);

                        });
                        var text = `
                        <div class="col-md-12">
                            <button type="button" id="btnDarDeBaja" class="btn btn-primary pull-right">Dar de baja</button>
                            <button type="button" id="btnRenovar" class="btn btn-primary pull-right" style="margin-right: 10px;">Renovar</button>
                        </div>
                        `;
                        $("#espacio_botones").append(text);
                    }else{
                        abrirModal("Error","El empleado no tiene asignado un puesto", "");
                    }
                }
            });
        }


    });

});
