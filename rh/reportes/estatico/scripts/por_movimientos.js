$gmx(document).ready(function(){
    $("#btnGenerarReporte").click(generar_reporte);
    $("#Movimiento").change(function(){ sel_alta_o_baja(); });
});

function generar_reporte(){
    if(validarFormulario($("#formularioPorMovimientos")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/reportes/generar_reporte_por_movimiento",
            data: $("#formularioPorMovimientos, #idPersona").serialize(),
            success: function(data){
                if(data.respuesta){
                    var urlDescarga = data.url_descarga;
                    $("#btnDescargarReporte").show();
                    $("#btnDescargarReporte").wrap('<a href="' + urlDescarga + '" download></a>');
                    abrirModal("Reporte generado", `El reporte ha sido creado correctamente`, "");
                }
                else{
                    abrirModal("Reporte no generado", `No existen movimientos`, "");
                    $("#btnDescargarReporte").hide();
                    $('#btnDescargarReporte').unwrap();
                }
            }
        });
    }
}

function sel_alta_o_baja(){
    if($("#Movimiento").val() == "1" || $("#Movimiento").val() == "2"){
        $("#NumEmpleado").show();
        $("#NumEmpleado").val("");
        $("#NumeroBuscarEmpleado").addClass("obligatorio");
    }else{
        $("#NumEmpleado").hide();
        $("#NumEmpleado").val("");
        $("#NumeroBuscarEmpleado").removeClass("obligatorio");
    }
}