$gmx(document).ready(function () {
    $("#btnGenerarResumen").click(generar_resumen);
    $("#btnConfirmarNomina_modal").click(confirma_nomina);    
});

function abrirAdModal() {    
    $("#MensajeAdModal").html("En realidad desea confirmar la nómina");
    $("#GenerarNominaModal").modal('show');
}

function confirma_nomina(){
    $("#GenerarNominaModal").modal('hide');
    window.document.getElementById("idNomina").disabled = "";
    $.ajax({
        async: false,
        type: "POST",
        url: "/nomina/confirmar_nomina",
        data: $("#formulario_resumen_nomina").serialize(),
        success: function (data) {
            if(data.respuesta == 1){
                window.document.getElementById("btnConfirmar").style.display = "none";
                window.document.getElementById("btnGenerarResumen").style.display = "none";
                window.document.getElementById("idNomina").disabled = "disabled";
                abrirModal("Confirmar nómina", "La nómina se confirmo correctamente.", "");
            }else{
                abrirModal("Confirmar nómina", "Error: Confirmación incorrecta.\nVeriricar error con sistemas.", "");
            }            
        }
        });
}

function generar_resumen() {

    if (validarFormulario($("#formulario_resumen_nomina")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/genera_resumen_nomina",
            data: $("#formulario_resumen_nomina").serialize(),
            success: function (data) {
                if (data.respuesta == 1) {
                    window.document.getElementById("idNomina").disabled = "disabled";
                    var TotalP = 0;
                    var TotalD = 0;
                    $("#tblNomina").show();       
                    $("#tblNomina tbody").empty();
                    data.listanomina.forEach(function(concepto) {
                        text = `
                        <tr>
                            <td>
                                ${concepto.idConcepto}
                            </td>  
                            <td>
                                ${concepto.Concepto}
                            </td>
                            <td>
                                ${concepto.Empleados}
                            </td>
                            <td class='text-right'>
                                ${concepto.Importe}
                            </td>
                        </tr>
                        `;
                        $("#tblNomina tbody").append(text);
                        if(concepto.idConcepto != "DT"){
                            if (concepto.Importe > 0){
                                TotalP = TotalP + parseFloat(concepto.Importe);
                            }else{
                                TotalD = TotalD + parseFloat(concepto.Importe);
                            }
                        }
                                            
                    });
                    text = "";
                    text = text + "<tr>";
                    text = text + "<td colspan='3'><label>Total de percepciones</label></td>";
                    text = text + "<td class='text-right'><label>"+TotalP.toFixed(2).toLocaleString("es-MX")+"</label></td>;"
                    text = text + "</tr>";
                    text = text + "<tr>";
                    text = text + "<td colspan='3'><label>Total de deducciones</label></td>";
                    text = text + "<td class='text-right'><label>"+Number(TotalD.toFixed(2))+"</label></td>;"
                    text = text + "</tr>";
                    text = text + "<tr>";
                    text = text + "<td colspan='3'><label>&nbsp;</label></td>";
                    text = text + "<td class='text-right'><label>"+ Number(TotalP+TotalD).toFixed(2) +"</label></td>";
                    text = text + "</tr>";
                    var urlDescarga = data.url_descarga;
                    text = text + "<tr>";
                    text = text + "<td colspan='2'><a href='"+urlDescarga+"' download class='btn btn-danger'>Descargar</a></td>";
                    text = text + "<td colspan='2'><button class='btn btn-danger' data-toggle='modal' data-target='#foo' type='button' id='btnConfirmar' onclick='abrirAdModal()' >Confirmar nómina</button></td>";
                    text = text + "</tr>";
                    $("#tblNomina tbody").append(text);                 
                }
                else{
                    $("#tblNomina").show();  
                    $("#tblNomina tbody").empty();
                    text = "";                
                    text = text + "<tr>";
                    text = text + "<td colspan='4'><label>No se encontraron registros</label></td>";
                    text = text + "</tr>";
                    $("#tblNomina tbody").append(text);
                }
            }
        });
    }else{
        $("#tblNomina").hide();       
        $("#tblNomina tbody").empty();
    }
}