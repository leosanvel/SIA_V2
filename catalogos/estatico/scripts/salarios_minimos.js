$gmx(document).ready(function(){
    inicializar_anio();
    obtener_salarios_minimos();

    $("#AnioFiscal").change(function(){
        obtener_salarios_minimos();
    });

    $("#btnGuardarSalariosMinimos").click(function(){
        guardar_salarios_minimos();
    });
});

function inicializar_anio(){
    var hoy = new Date();
    var anio = hoy.getFullYear();
    $("#AnioFiscal").val(anio);
}

function obtener_salarios_minimos(){
    if($("#AnioFiscal").val() != 0){
        $.ajax({
            type: "POST",
            url: "/catalogos/salarios-minimos/obtener-salarios-minimos",
            data: {
                AnioFiscal: $("#AnioFiscal").val()
            },
            success: function(data){
                if(data.SalariosMinimos){
                    $("#MontoDiario").val(data.SalariosMinimos.MontoDiario);
                    $("#MontoMensual").val(data.SalariosMinimos.MontoMensual);
                    $("#MontoAnual").val(data.SalariosMinimos.MontoAnual);
                }else{
                    $("#MontoDiario").val("");
                    $("#MontoMensual").val("");
                    $("#MontoAnual").val("");
                }
            }
        });
    }
}

function guardar_salarios_minimos(){
    if(validarFormulario($("#formularioSalariosMinimos")).valido){
        $.ajax({
            type: "POST",
            url: "/catalogos/salarios-minimos/guardar-salarios-minimos",
            data: $("#formularioSalariosMinimos").serialize(),
            success: function(data){
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
        });
    }
}