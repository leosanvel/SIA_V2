$gmx(document).ready(function(){
    //$("#btnGenerarContrato").click(generar_contrato);
    $("#btnGenerarContrato").click(ProcesandoArchivoNomina);
});

function generar_contrato(){
    //event.preventDefault();
    window.document.getElementById("btnGenerarContrato").disabled = "";
    $.ajax({
        async: false,
        type: "POST",
        url: "/RH/generarContrato",
        data: $("#formularioContrato").serialize(),
        success: function(data){
            window.document.getElementById("ImgModal").style.display = "none";
            if(data.generado){
                abrirModal("Contrato Generado", "Contrato generado de forma correcta", "");
            }
            
            var urlDescarga = data.url_descarga;
            $("#btnDescargaContrato").show();
            $("#btnDescargaContrato").wrap('<a href="' + urlDescarga + '"download></a>');
        }
    });
}

function ProcesandoArchivoNomina(){
    $("#btnDescargaContrato").hide();
    window.document.getElementById("btnGenerarContrato").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generar_contrato, 2000);
}