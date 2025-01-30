$gmx(document).ready(function(){
    inicializar_anio();
    obtener_quincenas();
    $("#btnGenerarReporte").click(generar_reporte);
    $("#Movimiento").change(function(){ sel_alta_o_baja(); });
    $("#Periodo").change(function(){
        obtener_quincenas();
    });
});

function inicializar_anio(){
    var hoy = new Date();
    var anio = hoy.getFullYear();
    $("#Periodo").val(anio);
}

function obtener_quincenas(){
    AnioFiscal = $("#Periodo").val();
    if($("#Periodo").val != ""){
        $.ajax({
            type: "POST",
            url: "/rh/reportes/por-movimientos/obtener-quincenas",
            data: {
                AnioFiscal: AnioFiscal
            },
            success: function(data){
                if(data.length > 0){
                    $("EQuincena").text("");
                    $("#Quincena").find('option').not(':first').remove();
                    data.forEach(function(Quincena){
                        $("#Quincena").append(new Option(Quincena.Descripcion, Quincena.idQuincena));
                    });
                }else{
                    $("EQuincena").text("No hay quincenas disponibles.");
                }
            }
        });
    }
}

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
    }else{
        $("#NumEmpleado").hide();
        $("#NumEmpleado").val("");
    }
}