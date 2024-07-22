$gmx(document).ready(function(){

});

function editar_aceptar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        $("#TipoIncidencia" + data).attr("readonly", false);
        $("#ActTipoIncidencia" + data).attr("disabled", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_tipoincidencia(data);
    }
}

function cancelar(data1, data2, data3) {
    //$("#idEstNivEsc" + data1).attr("readonly", true);
    $("#TipoIncidencia" + data1).attr("readonly", true);
    $("#ActTipoIncidencia" + data1).attr("disabled", true);

    //$("#idEstNivEsc" + data1).val(data3);
    $("#TipoIncidencia" + data1).val(data2);
    $("#ActTipoIncidencia" + data1).val(data3);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_tipoincidencia(dato){
    datos = {}
    datos["idTipoIncidencia"] = dato;
    datos["TipoIncidencia"] = $("#TipoIncidencia" + dato).val();
    datos["Activo"] = $("#ActTipoIncidencia" + dato).val();
    datos = JSON.stringify(datos);

    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/guardar_tipoincidencia",
        datatype: "json",
        contentType: "application/json; charset=utf-8",
        data: datos,
        success: function(data){
            if(data.guardado){
                abrirModal("Información guardada", "Los datos de Tipo de Incidencia se guardaron correctamente.", "recargar");
            }
        }
    });
}