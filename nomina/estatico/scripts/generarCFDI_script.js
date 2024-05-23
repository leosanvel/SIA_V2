$gmx(document).ready(function () {
    $("#btnGenerarCFDI").click(abrirAdModal);
    $("#btnGenerarCFDI_modal").click(generarCFDI);
});

function abrirAdModal() {
    if (validarFormulario($("#formularioGenerarCFDI")).valido) {
        $("#MensajeAdModal").html("¿Está seguro que desea generar el CFDI de la quincena " + $("#idNomina").val() + "?");
        $("#GenerarCFDIModal").modal('show');
    }
}


function generarCFDI() {
    console.log("GENERANDO CFDI")
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/crearCFDI",
        data: $("#formularioGenerarCFDI").serialize(),
        success: function (data) {
            console.log("TERMINADO")
            $("#GenerarCFDIModal").modal('hide');

            if (data.respuesta == "1") {
                abrirModal("CFDI", "Los archivos fueron creados correctamente.", "");
                var urlDescarga = data.url_descarga;
                $("#btnDescargaZIP ").show();
                $("#btnDescargaZIP ").wrap('<a href="' + urlDescarga + '" download></a>');
            }
        }
    });
}