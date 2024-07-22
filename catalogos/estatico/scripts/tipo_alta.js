$gmx(document).ready(function() {
   
});

function editar_aceptar(data) {
    if ($("#Editar_Aceptar" + data).text() == "Editar") {
        $("#TipoEmpleado" + data).attr("disabled", false);
        $("#TipoAlta" + data).attr("readonly", false);
        $("#ActTipoAlta" + data).attr("disabled", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else {
        guardar_modificar_tipoalta(data);
    }
}

function cancelar(data1, data2, data3, data4) {
    $("#TipoEmpleado" + data1).attr("disabled", true);
    $("#TipoAlta" + data1).attr("readonly", true);
    $("#ActTipoAlta" + data1).attr("disabled", true);
    $("#TipoEmpleado" + data1).val(data2);
    $("#TipoAlta" + data1).val(data3);
    $("#ActTipoAlta" + data1).val(data4);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_tipoalta(dato){
    valform = 0;
    if(!dato){
        index = ""
        if(validarFormulario($("#formularioTipoAlta")).valido){
            valform = 1;
            activo = ($("#ActTipoAlta" + index).val()) - 1;
        }else{
            valform = 0;
        }
    }else{
        index = dato;
        activo = $("#ActTipoAlta" + index).val();
    }
    if(valform || (index != "")){
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/guardar_Tipoalta",
            data: {
                "idTipoAlta": dato,
                "idtipoempleado": $("#TipoEmpleado" + index).val(),
                "TipoAlta": $("#TipoAlta" + index).val(),
                "activo": activo,
            },
            success: function(data){
                if(data.guardado){
                    abrirModal("Información guardada", "Los datos de Tipo de alta se guardaron correctamente", "recargar");
                }
            }
        });
    }
}