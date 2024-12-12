$gmx(document).ready(function(){
    $("#btnGuardaPension").click(function(){
        guardar_pension();
    });
});

function funcionSeleccionar(){
    buscar_pensiones();
    $("#formularioPension").show();
}

function buscar_pensiones(){
    if($("#idPersona").val() != ""){
        $.ajax({
            type: "POST",
            url: "/prestaciones/pensiones/buscar-pensiones",
            data: {
                idPersona: $("#idPersona").val(),
            },
            success: function(data){
                console.log(data);
                if(data.pensiones.length > 0){
                    $("#EResultadoPensiones").text("");
                    $("#tablaResultadosPensiones").show();
                    // Limpiar la tabla existente
                    $("#tablaResultadosPensiones tbody").empty();
                    data.pensiones.forEach(function(pension){
                        var texto = `
                            <tr>
                                <td>
                                    <input type="text" class="form-control" id="NumeroEmpleado${pension.idEmpleadoPension}" value="${pension.NumeroEmpleado}" style="width: 100px;" readonly>
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="NombreBeneficiario${pension.idEmpleadoPension}" value="${pension.NombreBeneficiario}" style="width: 450px;" readonly>
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="RFC${pension.idEmpleadoPension}" value="${pension.RFC}" style="width: 200px;" readonly>
                                </td>
                                <td>
                                    <input type="text" class="form-control" id="ClabeBancaria${pension.idEmpleadoPension}" value="${pension.ClabeBancaria}" style="width: 200px;" readonly>
                                </td>
                                <td>
                                    <textarea rows="3" class="form-control" id="descripcion${pension.idEmpleadoPension}" style="resize: none; width: 350px;" readonly>${pension.Observaciones}</textarea>
                                </td>
                            </tr>
                        `;
                        $("#tablaResultadosPensiones tbody").append(texto);
                    });
                }else{
                    $("#EResultadoPensiones").text("No se encontraron pensiones.");
                }
            }
        });
    }
}

function guardar_pension(){
    var ValidaEmpleado = true;
    var ExisteEmpleado = $("#idPersona").length > 0;
    if(!ExisteEmpleado || $("#idPersona").val() === ""){
        var ValidaEmpleado = false;
        $("#NumeroBuscarEmpleado").addClass("form-control-error");
        $("#ENumEmp").text("Seleccione un empleado.");
    }
    if(validarFormulario($("#formularioPension")).valido && ValidaEmpleado){
        $.ajax({
            type: "POST",
            url: "/prestaciones/pensiones/guardar-pension",
            data: $("#formularioPension, #idPersona").serialize(),
            success: function(data){
                if(data.respuesta == 1){
                    abrirModal("Ya existe un dato similar", "Ya existe un registro con un Nombre de beneficiario identico.", "");
                }else if(data.respuesta == 2){
                    abrirModal("Error al guardar", "No se pudo guardar la información.", "");
                }else if(data.respuesta == 99){
                    abrirModal("Guardado exitoso", "La información se guardo de forma correcta.", "recargar");
                }
            }
        });
    }
}