$gmx(document).ready(function(){
    $("#btnGuardarAnioFiscal").click(function(){
        guardar_Anio_Fiscal();
    });
});

function guardar_Anio_Fiscal(){
    if(validarFormulario($("#formularioAnioFiscal")).valido){
        $.ajax({
            type: "POST",
            url: "/catalogos/anio-fiscal/guardar-anio-fiscal",
            data: $("#formularioAnioFiscal").serialize(),
            success: function(data){
                if(data.respuesta == 0){
                    abrirModal("Error", "Ocurrió un error al procesar la información.", "");
                }
                if(data.respuesta == 1){
                    abrirModal("Error", "Ya existe registrado el año ingresado.", "");
                }
                if(data.respuesta == 2){
                    abrirModal("Error", "No se pudo guardar la información.", "");
                }
                if(data.respuesta == 99){
                    abrirModal("Guardado correcto", "Se guardo correctamente el año ingresado.", "recargar");
                }
            }
        });
    }
}