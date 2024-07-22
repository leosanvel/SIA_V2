$gmx(document).ready(function () {

});

function editar_aceptar(data) {
    if ($("#Editar_Aceptar" + data).text() == "Editar") {
        $("#sancion" + data).attr("readonly", false);
        $("#Activo" + data).attr("disabled", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else {
        guardar_modificar_tiposancion(data);
    }
}

function cancelar(data1, data2, data3) {
    $("#sancion" + data1).attr("readonly", true);
    $("#Activo" + data1).attr("disabled", true);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_tiposancion(idSancion) {
    datos = {}
    if (idSancion) {
        var valido = ($("#sancion" + idSancion).val()) ? true : false;
        datos["idSancion"] = idSancion;
        datos["Sancion"] = $("#sancion" + idSancion).val();
        datos["Activo"] = ($("#Activo" + idSancion).val());
        console.log(datos["Activo"] )
        datos = JSON.stringify(datos);
    }
    else {
        valido = validarFormulario($("#formularioAgregarSancion")).valido
        datos["Sancion"] = $("#Sancion").val();
        console.log(datos["Sancion"])
        datos["Activo"] = $("#Activo").val() - 1;
        datos = JSON.stringify(datos);
    }

    if (valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/catalogos/guardar_tiposancion",
            datatype: "json",
            contentType: "application/json; charset=utf-8",
            data: datos,
            success: function (data) {
                if (data.guardado) {
                    abrirModal("Información guardada", "Los datos de Tipo de Sanción se guardaron correctamente.", "recargar");
                }
            }
        })
    }
}