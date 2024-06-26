$gmx(document).ready(function() {
   
});

function activar_editar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        //$("#idNacionalidad" + data).attr("readonly", false);
        $("#Nacionalidad" + data).attr("readonly", false);
        $("#idNacionalidadFP" + data).attr("readonly", false);
        $("#idPaisFP" + data).attr("readonly", false);
        $("#ActNacionalidad" + data).attr("disabled", false);
        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_nacionalidad(data);
    }
}

function cancelar(data1, data2, data3, data4, data5){
    $("#Nacionalidad" + data1).attr("readonly", true);
    $("#idNacionalidadFP" + data1).attr("readonly", true);
    $("#idPaisFP" + data1).attr("readonly", true);
    $("#ActNacionalidad" + data1).attr("disabled", true);
    $("#Nacionalidad" + data1).val(data2);
    $("#idNacionalidadFP" + data1).val(data3);
    $("#idPaisFP" + data1).val(data4);
    $("#ActNacionalidad" + data1).val(data5);
    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_nacionalidad(dato){
    valform = 0;
    if(!dato){
        index = "";
        if(validarFormulario($("#formularioNacionalidad")).valido){
            valform = 1;
            activo = ($("#ActNacionalidad" + index).val()) - 1;
        }else{
            valform = 0;
        }
    }else{
        index = dato;
        activo = ($("#ActNacionalidad" + index).val());
    }
    if(valform || (index != "")){
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/guardar_nacionalidad",
            data:{
                "idNacionalidad": dato,
                "Nacionalidad": $("#Nacionalidad" + index).val(),
                "idNacionalidadFP": $("#idNacionalidadFP" + index).val(),
                "idPaisFP": $("#idPaisFP" + index).val(),
                "Activo": activo
            },
            success: function(data){
                if(data.guardado){
                    abrirModal("Información guardada", "Los datos de Nacionalidad se guardaron correctamente", "recargar");
                }
            }
        });
    }
}