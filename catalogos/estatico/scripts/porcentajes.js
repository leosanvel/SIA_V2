$gmx(document).ready(function () {

});

function editar_aceptar(data) {
    if ($("#Editar_Aceptar" + data).text() == "Editar") {
        $("#Activo" + data).attr("disabled", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else {
        guardar_modificar_porcentaje(data);
    }
}

function cancelar(data1) {
    $("#Activo" + data1).attr("disabled", true);
    
    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_porcentaje(dato) {
    datos = {}
    if (dato) {
        datos["idPorcentaje"] = dato;
        datos["Porcentaje"] = $("#porcentaje" + dato).val();
        datos["Activo"] = $("#Activo" + dato).val();
        var valido = ($("#porcentaje" + dato).val()) ? true : false;
        datos = JSON.stringify(datos);
    }
    else {
        datos["Porcentaje"] = $("#porcentaje").val();
        console.log(datos["Porcentaje"])
        datos["Activo"] = $("#Activo").val() - 1;
        datos = JSON.stringify(datos);
        valido = validarFormulario($("#formularioPorcentajes")).valido
    }

    if (valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/guardar_porcentajes",
            datatype: "json",
            contentType: "application/json; charset=utf-8",
            data: datos,
            success: function (data) {
                if (data.guardado) {
                    abrirModal("Información guardada", "Los datos de Tipo de Justificante se guardaron correctamente.", "recargar");
                }
            }
        })
    }
}