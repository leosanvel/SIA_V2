$gmx(document).ready(function(){
    inicializar_anio();
    inicializacion();
    $("#btnGenerarQuincenas").click(generar_quincenas);

    $("#AnioFiscal").change(function(){
        inicializacion();
    });
});

function inicializar_anio(){
    var hoy = new Date();
    var anio = hoy.getFullYear();
    $("#AnioFiscal").val(anio);
}

function inicializacion(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/quincenas/cargar-quincenas",
        data: {
            AnioFiscal: $("#AnioFiscal").val()
        },
        success: function(data){
            console.log(data);
            if(data.length > 0){
                $("#EResultadosQuincenas").text("");
                $("#tablaResultadosQuincenas").show();
                $("#tablaResultadosQuincenas tbody").empty();
                $("#btnGenerarQuincenas").hide();
                data.forEach(function(Quincena){
                    var FechaInicioFormateada = convertirFechaParaVisualizacion(Quincena.FechaInicio);
                    var FechaFinFormateada = convertirFechaParaVisualizacion(Quincena.FechaFin);
                    text = `
                    <tr>
                        <td>
                            <input type="text" class="form-control" id="Quincena${Quincena.idQuincena}" value="${Quincena.Quincena}" style="width: 100px;" readonly>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="FechaInicio${Quincena.idQuincena}" value="${FechaInicioFormateada}" readonly>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="FechaFin${Quincena.idQuincena}" value="${FechaFinFormateada}" readonly>
                        </td>
                        <td>
                            <input type="text" class="form-control" id="Descripcion${Quincena.idQuincena}" value="${Quincena.Descripcion}" readonly>
                        </td>
                        <td>
                            <button type="button" class="btn btn-primary oculta-empleado" id="Editar_Aceptar${Quincena. idQuincena}" onclick="editar_aceptar('${Quincena.idQuincena}')">Editar</button>
                        </td>
                        <td>
                            <button type="button" class="btn btn-primary oculta-empleado" id="Cancelar${Quincena.idQuincena}" onclick="cancelar('${Quincena.idQuincena}', '${Quincena.Fechas}', '${Quincena.Descripcion}')" style="display: none;">Cancelar</button>
                        </td>
                    </tr>
                    `;
                    $("#tablaResultadosQuincenas tbody").append(text);
                });
            }else{
                $("#EResultadosQuincenas").text("No hay quincenas generadas para este año fiscal.");
                $("#tablaResultadosQuincenas").hide();
                $("#tablaResultadosQuincenas tbody").empty();
                $("#btnGenerarQuincenas").show();
            }
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
        url: "/Catalogos/guardar_quincenas",
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

function generar_quincenas(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/quincenas/generar-quincenas",
        data: {
            AnioFiscal: $("#AnioFiscal").val()
        },
        success: function(data){
            if(data.respuesta == 1){
                abrirModal("Error", "No se ingresó un año válido.", "");
            }
            if(data.respuesta == 2){
                abrirModal("Error", "Hubo un error al generar las quincenas.", "");
            }
            if(data.respuesta == 99){
                abrirModal("Quincenas generadas", "Las quincenas para el año fiscal " + $("#AnioFiscal").val() + " se han generado correctamente.", "recargar");
            }
        }
    });
}