$gmx(document).ready(function(){
    $("#btnGenerarReporte").click(generar_reporte);
});

function generar_reporte(){
    if(validarFormulario($("#formularioPorMovimientos")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/reportes/generar_reporte_por_movimiento",
            data: $("#formularioPorMovimientos").serialize(),
            success: function(data){
                if(data.respuesta){
                    abrirModal("Reporte generado", `El reporte ha sido creado correctamente`, "");
                }
                else{
                    abrirModal("Reporte no generado", `No existen movimientos`, "");
                }
                var urlDescarga = data.url_descarga;
                $("#btnDescargarReporte").show();
                $("#btnDescargarReporte").wrap('<a href="' + urlDescarga + '" download></a>');
            }
        });
    }
}