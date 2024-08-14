$gmx(document).ready(function(){
    $("#btnGenerarReporte").click(ProcesandoReporte);
});

function generar_reporte(){
    if(validarFormulario($("#frmGeneralQuincena")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/prestaciones/genera-reporte-general-quincena",
            data: $("#frmGeneralQuincena").serialize(),
            success: function(data){
                window.document.getElementById("Quincenas").disabled = "";
                window.document.getElementById("btnGenerarReporte").disabled = "";
                window.document.getElementById("ImgModal").style.display = "none";
                if(data.respuesta){
                    var urlDescarga = data.url_descarga;
                    $("#btnDescargarReporte").show();
                    $("#btnDescargarReporte").wrap('<a href="' + urlDescarga + '" download></a>');
                    abrirModal("Reporte generado", "El reporte ha sido creado correctamente", "");
                }else{
                    abrirModal("Reporte no generado", "No se encontraron empleados", "");
                }
            }
        });
    }
}

function ProcesandoReporte(){
    window.document.getElementById("Quincenas").disabled = "disabled";
    window.document.getElementById("btnGenerarReporte").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generar_reporte, 2000);
}