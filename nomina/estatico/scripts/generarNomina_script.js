$gmx(document).ready(function () {
    $("#btnGenerarNomina").click(abrirAdModal);
    $("#btnGenerarNomina_modal").click(generarNomina);
    $('#calendar').datepicker();
});

function abrirAdModal() {
    if (validarFormulario($("#formularioGenerarNomina")).valido) {
        $("#MensajeAdModal").html("Se va ha correr la nómina " + $("#idNomina").val());
        $("#GenerarNominaModal").modal('show');
    }
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
                $("#tblNomina").show();       
                $("#tblNomina tbody").empty();
                data.listanomina.forEach(function(concepto) {
                    text = `
                    <tr>  
                        <td>
                            <label>${concepto.idConcepto}</label>
                        </td>
                        <td>
                            <label>${concepto.Empleados}</label>
                        </td>
                        <td>
                            <label>${concepto.Importe}</label>
                        </td>
                    </tr>
                    `;
                    $("#tblNomina tbody").append(text);
                });
            }
            else{                
                abrirModal("Error", "La nómina no fue procesada.", "");                
            }            
        }
    });
}