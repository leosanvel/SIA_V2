$gmx(document).ready(function() {
    //$("#guardarEstCiv").click(guardar_modificar_estadocivil());
});

function activar_editar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        //$("#idEstCiv" + data).attr("readonly", false);
        $("#EstCiv" + data).attr("readonly", false);
        $("#ActEstCiv" + data).attr("disabled", false);
        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_estadocivil(data);
    }
}

function cancelar(data1, data2, data3){
    $("#EstCiv" + data1).attr("readonly", true);
    $("#ActEstCiv" + data1).attr("disabled", true);
    $("#EstCiv" + data1).val(data2);
    $("#ActEstCiv" + data1).val(data3);
    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_estadocivil(dato){
    valform = 0;
    if(!dato){
        index = "";
        if(validarFormulario($("#formularioEstadoCivil")).valido){
            valform = 1;
            activo = ($("#ActEstCiv" + index).val()) - 1;
        }else{
            valform = 0;
        }
    }else{
        index = dato;
        activo = $("#ActEstCiv" + index).val();
    }
    if(valform || (index != "")){
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/guardar_estadocivil",
            data: {
                "idEstadoCivil": dato,
                "EstadoCivil": $("#EstCiv" + index).val(),
                "Activo": activo
            },
            success: function(data){
                if(data.guardado){
                    abrirModal("Información guardada", "Los datos de Estado civil se guardaron correctamente.", "recargar");
                }
            }
        });
    }
}