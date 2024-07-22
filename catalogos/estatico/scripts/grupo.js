$gmx(document).ready(function() {
   $("#TipEmp").change(cargarTipAlt);
   $("#ModTipEmp").change(cargarModTipAlt);
   $("#ModTipAlt").change(cargarGrupo);
});

function cargarTipAlt(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/select_TipAlt",
        data: {
            "idTipoEmpleo": $("#TipEmp").val()
        },
        success: function(data){
            $("#idTipAlt").html(data);
        }
    });
}

function cargarModTipAlt(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/select_TipAlt",
        data: {
            "idTipoEmpleo": $("#ModTipEmp").val()
        },
        success: function(data){
            $("#ModTipAlt").html(data);
        }
    });
}

function cargarGrupo(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/cargar_Grupo",
        data: {
            "TipEmp": $("#ModTipEmp").val(),
            "TipAlt": $("#ModTipAlt").val()
        },
        success: function(data){
            $("#TabModGrupo").html(data);
        }
    });
}

function editar_aceptar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        $("#idTipAlt" + data).attr("readonly", false);
        $("#Grupo" + data).attr("readonly", false);
        $("#ActGrupo" + data).attr("disabled", false);
        $("#idEsqHon" + data).attr("readonly", false);
        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_grupo(data);
    }
}

function cancelar(data1, data2, data3, data4, data5){
    $("#idTipAlt" + data1).attr("readonly", true);
    $("#Grupo" + data1).attr("readonly", true);
    $("#ActGrupo" + data1).attr("disabled", true);
    $("#idEsqHon" + data1).attr("readonly", true);
    $("#idTipAlt" + data1).val(data2);
    $("#Grupo" + data1).val(data3);
    $("#ActGrupo" + data1).val(data4);
    $("#idEsqHon" + data1).val(data5);
    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_grupo(dato){
    valform = 0;
    if(!dato){
        index = "";
        if(validarFormulario($("#formularioGrupo")).valido){
            valform = 1;
            activo = ($("#ActGrupo" + index).val()) - 1;
        }else{
            valform = 0;
        }
    }else{
        index = dato;
        activo = $("#ActGrupo" + index).val();
    }
    if(valform || (index != "")){
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/guardar_Grupo",
            data: {
                "idGrupo": dato,
                "idTipoAlta": $("#idTipAlt" + index).val(),
                "Grupo": $("#Grupo" + index).val(),
                "Activo": activo,
                "idEsquemaHonorarios": $("#idEsqHon" + index).val()
            },
            success: function(data){
                if(data.guardado){
                    abrirModal("Información guardada", "Los datos de Grupo se guardaron correctamente.", "recargar");
                }
            }
        });
    }
}