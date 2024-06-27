$gmx(document).ready(function(){
    $("#btnGenerarChecador").click(ProcesandoChecador);
});

function generar_checador(event){
    //event.preventDefault();
    window.document.getElementById("NumQuincena").disabled = "";
    window.document.getElementById("btnGenerarChecador").disabled = "";
    if(validarFormulario($("#formularioGenerarChecador")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/generar-checador",
            data: $("#formularioGenerarChecador").serialize(),
            success: function(data){
                window.document.getElementById("ImgModal").style.display = "none";
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

function ProcesandoChecador(){
    window.document.getElementById("NumQuincena").disabled = "disabled";
    window.document.getElementById("btnGenerarChecador").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(generar_checador, 2000);
}