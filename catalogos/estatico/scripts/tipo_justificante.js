$gmx(document).ready(function(){

});

function editar_aceptar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        $("#TipoJustificante" + data).attr("readonly", false);
        $("#ActTipoJustificante" + data).attr("disabled", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_tipojustificante(data);
    }
}

function cancelar(data1, data2, data3) {
    //$("#idEstNivEsc" + data1).attr("readonly", true);
    $("#TipoJustificante" + data1).attr("readonly", true);
    $("#ActTipoJustificante" + data1).attr("disabled", true);

    //$("#idEstNivEsc" + data1).val(data3);
    $("#TipoJustificante" + data1).val(data2);
    $("#ActTipoJustificante" + data1).val(data3);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_tipojustificantes(dato){
    datos = {}
    datos["idTipoJustificante"] = dato;
    datos["TipoJustificante"] = $("#TipoJustificante" + dato).val();
    datos["ActTipoJustificante"] = $("#ActTipoJustificante" + dato).val();
    datos = JSON.stringify(datos);

    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/guardar_tipojustificante",
        datatype: "json",
        contentType: "application/json; charset=utf-8",
        data: datos,
        success: function(data){
            if(data.guardado){
                abrirModal("Información guardada", "Los datos de Tipo de Justificante se guardaron correctamente.", "recargar");
            }
        }
    })
}