$gmx(document).ready(function () {
    $("#btnGenerarCFDI").click(abrirAdModal);
    $("#btnGenerarCFDI_modal").click(generarCFDI);
    console.log("CARGADO");
});

function abrirAdModal() {
    console.log("Abrir modal");
    if (validarFormulario($("#formularioGenerarCFDI")).valido) {
        $("#MensajeAdModal").html("¿Está seguro que desea generar el CFDI de la quincena " + $("#NumQuincena").val() + "?");
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

            if (data.respuesta == "existente") {
                abrirModal("Archivo existente", "Los archivos fueron creados con anterioridad.", "");
            }

            if (data.respuesta == "creado") {
                abrirModal("Archivo Generado", "Los archivos han sido generados correctamente.", "");
            }


            // Manejar la respuesta JSON para obtener la URL de descarga
            var urlDescarga = data.url_descarga;
            $("#btnDescargaZIP ").show();
            // Crear un enlace de descarga dinámico
            $("#btnDescargaZIP ").wrap('<a href="' + urlDescarga + '" download></a>');
        }
    });
}