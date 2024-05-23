$gmx(document).ready(function () {
    $("#btnGenerarNomina").click(abrirAdModal);
    $("#btnGenerarNomina_modal").click(generarNomina);
});

function abrirAdModal() {
    if (validarFormulario($("#formularioGenerarNomina")).valido) {
        $("#MensajeAdModal").html("Se va ha correr la nómina " + $("#idNomina").val());
        $("#GenerarNominaModal").modal('show');
    }
}
function MostarNomina(listanomina){
    
        $("#tblNomina").show();
        
        $("#tblNomina tbody").empty();

        listanomina.forEach(function (concepto) {
            text = `
            <tr>  
                <td>
                    <label>"${concepto.Concepto}"</label>"
                </td>
                <td>
                    <label>"${concepto.Importe}"</label>"
                </td>
            </tr>
            `;
            $("#tblNomina tbody").append(text);
        });

}



function generarNomina() {
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/crearNomina",
        data: $("#formularioGenerarNomina").serialize(),
        success: function (data) {
            $("#GenerarNominaModal").modal('hide');
            
            if (data.respuesta == "1") {
                abrirModal("Archivo Generado", "La nómina se procesó correctamente.", "");
            }
            else{                
                abrirModal("Error", "La nómina no fue procesada.", "");                
            }
            MostarNomina(data.listanomina);

        }
    });
}