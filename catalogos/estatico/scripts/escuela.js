$gmx(document).ready(function() {
   $("#NivelEscolar").change(cargarEscuela);
   //$("#guardarEscuela").click(guardar_modificar_escuela());
});

function cargarEscuela(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/Catalogos/cargar_TabEscuela",
        data: {
            "NivEsc": $("#NivelEscolar").val()
        },
        success: function(data){
            $("#TabModEscuela").show();
            $("#TabModEscuela tbody").empty();
            data.forEach(function(Escuela){
                console.log(typeof(Escuela));
                text = `
                    <tr>
                    <td><input type="text" class="form-control" id="idEscuela${Escuela.idInstitucionEscolar}" value="${Escuela.idInstitucionEscolar}" readonly></td>
                    <td><input type="text" class="form-control" id="Escuela${Escuela.idInstitucionEscolar}" value='${Escuela.InstitucionEscolar}' readonly></td>
                    <td>
                        <select id="ActEscuela${Escuela.idInstitucionEscolar}" name="ActEscuela${Escuela.idInstitucionEscolar}" class="obligatorio form-control" disabled value=${Escuela.Activo}>
                            <option value="0">Inactivo</option>
                            <option value="1">Activo</option>
                        </select>
                        <script>
                            document.ready = document.getElementById("ActEscuela${Escuela.idInstitucionEscolar}").value = "${Escuela.Activo}"
                        </script>
                    </td>
                    <td><button type="button" class="btn btn-primary" id="Editar_Aceptar${Escuela.idInstitucionEscolar}" onclick="editar_aceptar(${Escuela.idInstitucionEscolar})">Editar</button></td>
                    <td><button type="button" class="btn btn-secondary" id="Cancelar${Escuela.idInstitucionEscolar}" onclick="cancelar(${Escuela.idInstitucionEscolar})" style="display: none">Cancelar</button></td>
                    `
                $("#TabModEscuela tbody").append(text); 
            });
            //$("#TabModEscuela tbody").append(data);
        }
    });
}

function editar_aceptar(data){
    if($("#Editar_Aceptar" + data).text() == "Editar"){
        //$("#idEscuela" + data).attr("readonly", false);
        $("#Escuela" + data).attr("readonly", false);
        $("#ActEscuela" + data).attr("disabled", false);
        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else{
        guardar_modificar_escuela(data);
    }
}

// function cancelar(data1, data2, data3){
//     //$("#idEscuela" + data1).attr("readonly", true);
//     $("#Escuela" + data1).attr("readonly", true);
//     $("#ActEscuela" + data1).attr("disabled", true);

//     //$("#idEscuela" + data1).val(data2);
//     $("#Escuela" + data1).val(data2);
//     $("#ActEscuela" + data1).val(data3);
//     $("#Editar_Aceptar" + data1).text("Editar");
//     $("#Cancelar" + data1).toggle();
// }

function cancelar(idInstitucionEscolar){
    $.ajax({
        async: false,
        type: "POST",
        url: "/Catalogos/buscar_escuela",
        data: {"idInstitucionEscolar": idInstitucionEscolar
        },
        success: function(Escuela){
            if(Escuela){
                //$("#idEscuela" + data1).attr("readonly", true);
                $("#Escuela" + Escuela.idInstitucionEscolar).attr("readonly", true);
                $("#ActEscuela" + Escuela.idInstitucionEscolar).attr("disabled", true);

                //$("#idEscuela" + data1).val(data2);
                $("#Escuela" + Escuela.idInstitucionEscolar).val(Escuela.InstitucionEscolar);
                $("#ActEscuela" + Escuela.idInstitucionEscolar).val(Escuela.Activo);
                $("#Editar_Aceptar" + Escuela.idInstitucionEscolar).text("Editar");
                $("#Cancelar" + Escuela.idInstitucionEscolar).toggle();
            }
        }
    });
    
}

function guardar_modificar_escuela(dato){
    valform = 0;
    if(!dato){
        index = "";
        if(validarFormulario($("#formularioEscuela")).valido){
            valform = 1;
            activo = ($("#ActEscuela" + index).val()) - 1;
        }else{
            valform = 0;
        }
    }else{
        index = dato;
        activo = $("#ActEscuela" + index).val();
    }
    //console.log(index);
    if(valform || (index != "")){
        $.ajax({
            async: false,
            type: "POST",
            url: "/Catalogos/guardar_escuela",
            data: {
                "idInstitucionEscolar": dato,
                "InstitucionEscolar": $("#Escuela" + index).val(),
                "Activo": activo,
                "idescolaridad": $("#NivelEscolar").val(),
            },
            success: function(data){
                if(data.guardado){
                    abrirModal("Información guardada", "Los datos de Escuela se guardaron correctamente.", "recargar");
                }
            }
        });
    }
}