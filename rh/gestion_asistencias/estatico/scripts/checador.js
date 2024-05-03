$gmx(document).ready(function(){
    $("#btnGenerarChecador").click(generar_checador);
});

function generar_checador(event){
    event.preventDefault();
    if(validarFormulario($("#formularioGenerarChecador")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/generar-checador",
            data: $("#formularioGenerarChecador").serialize(),
            success: function(data){
                if(data.guardado){
                    abrirModal("Checador generado", "Checador generado de forma correcta.", "recargar");
                }
                else{
                    abrirModal("Checador existente", "El checador de esta quincena ya se ha generado", "recargar");
                }
            }
        });
    }
}