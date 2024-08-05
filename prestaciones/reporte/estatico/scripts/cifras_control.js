$gmx(document).ready(function(){
    $("#btnGenerarReporte").click(generar_reporte);
});

function generar_reporte(){
    if(validarFormulario($("#formularioCifrasControl")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/prestaciones/reportes/generar-reporte-cifras-control",
            data: $("#formularioCifrasControl").serialize(),
            success: function(data){
                if(data.respuesta){
                    var urlDescarga = data.url_descarga;
                    $("#btnDescargarReporte").show();
                    $("#btnDescargarReporte").wrap('<a href="' + urlDescarga + '" download></a>');
                    abrirModal("Reporte generado", "El reporte ha sido creado correctamente", "");
                }else{
                    abrirModal("Reporte no generado", "No existen conceptos", "");
                }
            }
        });
    }
}