$gmx(document).ready(function(){
    inicializar_anio();
    obtener_tabulador_impuestos();

    $("#AnioFiscal").change(function(){
        obtener_tabulador_impuestos();
    });

    $("#btnGuardarTabuladorImpuestos").click(function(){
        guardar_tabulador_impuestos();
    });
});

function inicializar_anio(){
    var hoy = new Date();
    var anio = hoy.getFullYear();
    console.log(anio);
    $("#AnioFiscal").val(anio);
}

function obtener_tabulador_impuestos(){
    if($("#AnioFiscal").val() != "0"){
        $.ajax({
            type: "POST",
            url: "/catalogos/tabulador-impuestos/obtener-tabulador-impuestos",
            data: $("#formularioTabuladorImpuestos").serialize(),
            success: function(data){
                if(data.TabuladorImpuestos.length > 0){
                    var cont = 1;
                    data.TabuladorImpuestos.forEach(function(TabuladorImpuestos){
                        $(`#LimiteInferior${cont}`).val(TabuladorImpuestos.LimiteInferior);
                        $(`#LimiteSuperior${cont}`).val(TabuladorImpuestos.LimiteSuperior);
                        $(`#CuotaFija${cont}`).val(TabuladorImpuestos.CuotaFija);
                        $(`#Porcentaje${cont}`).val(TabuladorImpuestos.Porcentaje);
                        cont++;
                    });
                }else{
                    for(var cont = 1; cont <= 11; cont++){
                        $(`#LimiteInferior${cont}`).val("");
                        $(`#LimiteSuperior${cont}`).val("");
                        $(`#CuotaFija${cont}`).val("");
                        $(`#Porcentaje${cont}`).val("");
                    }
                }
            }
        })
    }
}

function guardar_tabulador_impuestos(){
    if(validarFormulario($("#formularioTabuladorImpuestos")).valido){
        $.ajax({
            type: "POST",
            url: "/catalogos/tabulador-impuestos/guardar-tabulador-impuestos",
            data: $("#formularioTabuladorImpuestos").serialize(),
            success: function(data){
                if(data){
                    if(data.respuesta == 1){
                        abrirModal("Error", "Hubo un error al guardar la información.", "");
                    }
                    if(data.respuesta == 98){
                        abrirModal("Información actualizada", "La información del año fiscal " + $("#AnioFiscal").val() + "  se ha actualizado correctamente.", "recargar");
                    }
                    if(data.respuesta == 99){
                        abrirModal("Información registrada", "La información del año fiscal " + $("#AnioFiscal").val() + "  se ha registrado correctamente.", "recargar");
                    }
                }
            }
        })
    }
}