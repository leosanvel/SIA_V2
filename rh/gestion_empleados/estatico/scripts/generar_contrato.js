$gmx(document).ready(function(){
    $("#btnGenerarContrato").click(generar_contrato);
});

function generar_contrato(){
    //event.preventDefault();
    $.ajax({
        async: false,
        type: "POST",
        url: "/RH/generarContrato",
        success: function(data){
            if(data.generado){
                abrirModal("Contrato Generado", "Contrato generado de forma correcta", "");
            }
            
            var urlDescarga = data.url_descarga;
            $("#btnDescargaContrato").show();
            $("#btnDescargaContrato").wrap('<a href="' + urlDescarga + '"download></a>');
        }
    });
}