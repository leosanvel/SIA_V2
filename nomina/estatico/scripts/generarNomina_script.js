$gmx(document).ready(function () {
    $("#btnGenerarNomina").click(abrirAdModal);
    $("#btnGenerarNomina_modal").click(ProcesandoNomina);
    $('#calendar').datepicker();
});

function abrirAdModal() {
    if (validarFormulario($("#formularioGenerarNomina")).valido) {
        $("#MensajeAdModal").html("Se va ha procesar la nómina " + $("#idNomina option:selected").text());
        $("#GenerarNominaModal").modal('show');
    }
}

function ProcesandoNomina(){
    $("#GenerarNominaModal").modal('hide');
    window.document.getElementById("idNomina").disabled = "disabled";
    window.document.getElementById("Observaciones").disabled = "disabled";
    window.document.getElementById("chkPV").disabled = "disabled";
    window.document.getElementById("btnGenerarNomina").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generarNomina, 3000);
}

function generarNomina() {
    window.document.getElementById("idNomina").disabled = "";
    window.document.getElementById("Observaciones").disabled = "";
    window.document.getElementById("chkPV").disabled = "";
    window.document.getElementById("btnGenerarNomina").disabled = "";
    window.document.getElementById("ImgModal").style.display = "none";
   $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/crearNomina",
        data: $("#formularioGenerarNomina").serialize(),
        success: function (data) {                      
            if (data.respuesta == "1") {
                abrirModal("Archivo Generado", "La nómina se procesó correctamente.", "");            
            }
            else{                
                abrirModal("Error", "La nómina no fue procesada.", "");                
            }
            window.document.getElementById("idNomina").value = 0;
            window.document.getElementById("Observaciones").value = "";
            window.document.getElementById("chkPV").checked = false;
        }
    });
}