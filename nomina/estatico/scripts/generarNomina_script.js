$gmx(document).ready(function () {
    $("#btnGenerarNomina").click(abrirAdModal);
    $("#btnGenerarNomina_modal").click(generarNomina);
});

function abrirAdModal() {
    if (validarFormulario($("#formularioGenerarNomina")).valido) {
        $("#MensajeAdModal").html("Se va ha correr la nómina " + $("#idNomina").val());
        $("#GenerarNominaModal").modal('show');
    }
}
function generarNomina() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/crearNomina",
        data: $("#formularioGenerarNomina").serialize(),
        success: function (data) {
            $("#GenerarNominaModal").modal('hide');
            
            if (data.respuesta == "1") {
                abrirModal("Archivo Generado", "La nómina se procesó correctamente.", "");
            }
            else{                
                abrirModal("Error", "La nómina no fue procesada.", "");
            }

        }
    });
}