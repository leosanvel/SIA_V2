$gmx(document).ready(function () {
    $("#btnGenerarArchivoNomina").click(abrirAdModal);
    $("#btnGenerarArchivoNomina_modal").click(ProcesandoArchivoNomina);
});

function abrirAdModal() {
    if (validarFormulario($("#formularioArchivoNomina")).valido) {
        $("#MensajeAdModal").html("Generar archivo de nómina");
        $("#GenerarArchivoNominaModal").modal('show');
    }
}

function ProcesandoArchivoNomina(){
    $("#GenerarArchivoNominaModal").modal('hide');
    $("#btnDescargar").hide();
    window.document.getElementById("idNomina").disabled = "disabled";
    window.document.getElementById("btnGenerarArchivoNomina").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generarArchivoNomina, 2000);
}

function generarArchivoNomina() {
    window.document.getElementById("idNomina").disabled = "";
    window.document.getElementById("btnGenerarArchivoNomina").disabled = "";
    window.document.getElementById("ImgModal").style.display = "none";
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/ArchivoNomina",
        data: $("#formularioArchivoNomina").serialize(),
        success: function (data) {
            $("#GenerarArchivoNominaModal").modal('hide');
            if (data.respuesta == 1) {
                var urlDescarga = data.url_descarga;
                abrirModal("Archivo de Nómina", "El archivo fue generado correctamente.", "");
                $("#btnDescargar ").show();
                $("#btnDescargar ").wrap('<a href="' + urlDescarga + '" download></a>');
            }else{
                abrirModal("Nómina", "El archivo no fue creado.", "");
            }
        }
    });
}