$gmx(document).ready(function () {
    $("#btnGenerarDispersion").click(abrirAdModal);
    $("#btnGenerarDispersion_modal").click(ProcesandoDispersion);
});

function abrirAdModal() {
    if (validarFormulario($("#formularioDispersion")).valido) {
        $("#MensajeAdModal").html("Generar archivo de dispersión");
        $("#GenerarDispersionModal").modal('show');
    }
}

function ProcesandoDispersion(){
    $("#GenerarDispersionModal").modal('hide');
    $("#btnDescargar ").hide();
    window.document.getElementById("idNomina").disabled = "disabled";
    window.document.getElementById("btnGenerarDispersion").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generarDispersion, 2000);
}

function generarDispersion() {
    window.document.getElementById("idNomina").disabled = "";
    window.document.getElementById("btnGenerarDispersion").disabled = "";
    window.document.getElementById("ImgModal").style.display = "none";
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/Dispersion",
        data: $("#formularioDispersion").serialize(),
        success: function (data) {
            $("#GenerarDispersionModal").modal('hide');
            if (data.respuesta == "1") {
                var urlDescarga = data.url_descarga;
                abrirModal("Dispersioón", "El archivo fue generado correctamente.", "");
                $("#btnDescargar ").show();
                $("#btnDescargar ").wrap('<a href="' + urlDescarga + '" download></a>');
            }else{
                abrirModal("Dispersión", "El archivo no fue creado.", "");
            }
        }
    });
}