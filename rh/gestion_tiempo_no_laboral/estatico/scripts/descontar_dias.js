$gmx(document).ready(function(){

    $("#btnGuardarDescontarDias").click(guardar_descontar_dias);
    
});

function guardar_descontar_dias(event){
    event.preventDefault();
    var validaEmpleado = true;
    var validaDias = true;
    var existeNumeroEmpleado = $("#idPersona").length > 0;

    if(!existeNumeroEmpleado || ($("#idPersona").val()) === ""){
        var validaEmpleado = false;
        $("#NumeroEmpleadoSeleccionado").addClass("form-control-error");
        $("#ENumEmp").text("Seleccione un empleado.");
    }
    console.log(parseInt($("#DescontarDias").val()) > 15);
    if(parseInt($("#DescontarDias").val()) > 15){
        validaDias = false;
        
    }else{
        validaDias = true;
        $("#EDescontarDias").text("");
    }
    console.log($("#EDescontarDias").text());
    if(validarFormulario($("#formularioDescontarDias")).valido && validaEmpleado){
        if(parseInt($("#DescontarDias").val()) <= 15){
            $.ajax({
                async: false,
                type: "POST",
                url: "/rh/gestion-tiempo-no-laboral/guardar-descontar-dias",
                data: $("#formularioDescontarDias, #idPersona").serialize(),
                success: function(data){
                    if(data){

                    }
                }
            });
        }else{
            $("#EDescontarDias").text("Solo se admiten hasta 15 días.");
        }
    }
}

function buscar_descontar_dias(){
    var idPersona = $("#idPersona").val()
    if(idPersona){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-tiempo-no-laboral/buscar-descontar-dias",
            data: {
                "idPersona": $("#idPersona").val()
            },
            success: function(data){
                if(data.descontar_dias_lista.length > 0){
                    $("#EResultado").text("");
                    $("#TablaResultadosDescontarDias").show();
                    $("#TablaResultadosDescontarDias tbody").empty();

                    var opcionesPorcentaje = '';
                        data.porcentajes.forEach(function (porcentaje) {
                            opcionesPorcentaje += `<option value="${porcentaje.idPorcentaje}">${porcentaje.Porcentaje}%</option>`;
                        });

                    var cont = 1;
                    data.descontar_dias_lista.forEach(function(descontar_dias){
                        text = `
                            <tr>
                                <td>
                                    <select id="porcentaje${cont}"
                                        name="Porcentaje${cont}"
                                        class="obligatorio form-control" readonly disabled>
                                        ${opcionesPorcentaje}
                                    </select>
                                </td>
                                <td><input type="text" class="form-control" id="Dias${cont}" value="${descontar_dias.Dias}" readonly></td>
                                <td>
                                    <div style="display: block;">
                                        <button type="button" class="btn btn-primary oculta-empleado" id="Eliminar${cont}" onclick="eliminar(${cont}, ${descontar_dias.idPersona}, ${descontar_dias.idQuincena}, ${descontar_dias.idPorcentaje}, ${descontar_dias.Dias})">Eliminar</button>
                                    </div>
                                </td>
                            </tr>
                        `;
                        $("#TablaResultadosDescontarDias tbody").append(text);
                        $(`#porcentaje${cont}`).val(descontar_dias.idPorcentaje);
                    });
                }else{
                    $("#EResultado").text("No se encontraron resultados");
                    $("#TablaResultadosDescontarDias").hide();
                    $("#TablaResultadosDescontarDias tbody").empty();
                }
            }
        });
    }
}

function eliminar(cont, idPersona, idQuincena, idPorcentaje, Dias){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-tiempo-no-laboral/eliminar-descontar-dias",
        data: {
            "idPersona": idPersona,
            "idQuincena": idQuincena,
            "idPorcentaje": idPorcentaje,
            "Dias": Dias
        },
        success: function(data){
            if(data.eliminado){
                abrirModal("Días a descontar eliminados", "Los días a descontar se han eliminado de manera correcta.", "recargar");
            }else{
                abrirModal("Días a descontar no eliminados", "Los días a descontar no se han podido eliminar.", "recargar");
            }
        }
    });
}

function funcionSeleccionar(){
    buscar_descontar_dias();
}