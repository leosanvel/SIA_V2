$gmx(document).ready(function(){
    inicializacion();
    $("#ActualizarFechas").click(actualizar_quincenas);
});

function inicializacion(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/cargar_quincenas",
        success: function(data){
            $("#TabQuincenas").show();
            $("#TabQuincenas tbody").empty();
            data.forEach(function(Quincena){
                var FechaInicioFormateada = convertirFechaParaVisualizacion(Quincena.FechaInicio);
                var FechaFinFormateada = convertirFechaParaVisualizacion(Quincena.FechaFin);
                text = `
                <tr>
                    <td><input type="text" class="form-control" id="Quincena${Quincena.idQuincena}" value="${Quincena.Quincena}" readonly></td>
                    <td><input type="text" class="form-control" id="Fechas${Quincena.idQuincena}" value="${Quincena.Fechas}" readonly></td>
                    <td><input type="text" class="form-control" id="FechaInicio${Quincena.idQuincena}" value="${FechaInicioFormateada}" readonly></td>
                    <td><input type="text" class="form-control" id="FechaFin${Quincena.idQuincena}" value="${FechaFinFormateada}" readonly></td>
                    <td><input type="text" class="form-control" id="Descripcion${Quincena.idQuincena}" value="${Quincena.Descripcion}" readonly></td>
                    <td><button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar${Quincena.idQuincena}" onclick="editar_aceptar('${Quincena.idQuincena}')">Editar</button></td>
                    <td><button type="button" class="btn btn-primary oculta-empleado" id="Cancelar${Quincena.idQuincena}" onclick="cancelar('${Quincena.idQuincena}', '${Quincena.Fechas}', '${Quincena.Descripcion}')" style="display: none;">Cancelar</button></td>
                </tr>
                `;
                $("#TabQuincenas tbody").append(text);
            });
        }
    });
}

function editar_aceptar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        $("#Fechas" + data).attr("readonly", false);
        $("#Descripcion" + data).attr("readonly", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_quincenas(data);
    }
}

function cancelar(data1, data2, data3){
    $("#Fechas" + data1).attr("readonly", true);
    $("#Descripcion" + data1).attr("readonly", true);

    $("#Fechas" + data1).val(data2);
    $("#Descripcion" + data1).val(data3);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_quincenas(dato){
    datos = {};
    datos["idQuincena"] = dato;
    datos["Fechas"] = $("#Fechas" + dato).val();
    datos["Descripcion"] = $("#Descripcion" + dato).val();
    datos = JSON.stringify(datos);
    
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/guardar_quincenas",
        datatype: "json",
        contentType: "application/json; charset=utf-8",
        data: datos,
        success: function(data){
            if(data.guardado){
                abrirModal("Información guardada", "Los datos de Quincenas se guardaron correctamente", "recargar");
            }
        }
    });
}

function actualizar_quincenas(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/actualizar_quincenas",
        success: function(data){
            if(data.guardado){
                abrirModal("Fechas actualizadas", "Las fechas de inicio y fin se han actualizado de forma correcta.", "recargar");
            }
        }
    });
}