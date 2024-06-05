$gmx(document).ready(function () {
    $("#btnGenerarCFDI").click(abrirAdModal);
    $("#btnGenerarCFDI_modal").click(ProcesandoNomina);
});

function abrirAdModal() {
    if (validarFormulario($("#formularioGenerarCFDI")).valido) {
        $("#MensajeAdModal").html("Se van a generar los archivos para su CFDI");
        $("#GenerarCFDIModal").modal('show');
    }
}

function ProcesandoNomina(){
    $("#GenerarCFDIModal").modal('hide');
    $("#btnDescargaZIP ").hide();
    window.document.getElementById("idNomina").disabled = "disabled";
    window.document.getElementById("btnGenerarCFDI").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generarCFDI, 3000);
}

function generarCFDI() {
    window.document.getElementById("idNomina").disabled = "";
    window.document.getElementById("btnGenerarCFDI").disabled = "";
    window.document.getElementById("ImgModal").style.display = "none";
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/crearCFDI",
        data: $("#formularioGenerarCFDI").serialize(),
        success: function (data) {
            $("#GenerarCFDIModal").modal('hide');
            if (data.respuesta == "1") {
                var urlDescarga = data.url_descarga;
                abrirModal("CFDI", "Los archivos fueron creados correctamente.", "");
                $("#btnDescargaZIP ").show();
                $("#btnDescargaZIP ").wrap('<a href="' + urlDescarga + '" download></a>');
            }else{
                abrirModal("CFDI", "Los archivos no fueron creados.", "");
            }
        }
    });
}