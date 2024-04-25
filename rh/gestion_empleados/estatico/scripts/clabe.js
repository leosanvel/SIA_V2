$gmx(document).ready(function(){
    $("#btnBuscaClabe").click(buscar_clabe);
});

function buscar_clabe(){
    if($("#NumeroBuscarEmpleado").val() != ""){
        $.ajax({
            async: false,
            type: "POST",
            url: "/RH/buscarClabe",
            data: {
                "idPersona": $("#idPersona").val()
            },
            success: function(data){
                if(data.length > 0){
                    $("#TabClabes").show();
                    $("#TabClabes tbody").empty();
                    $("#EResultadoClabes").text("");
                    var cont = 1;
                    data.forEach(function(clabe){
                        text = `
                            <tr>
                                <input type="hidden" id="idPersona${cont}" name="idPersona${cont}" value="${clabe.idPersona}">
                                <td><input type="text" class="form-control" id="Clabe${cont}" value="${clabe.Clabe}" style="width: 300px;" readonly></input></td>
                                <td>
                                    <select id="ActClabe${cont}" name="ActClabe${cont}" class="obligatorio form-control" value="${clabe.Activo}" disabled>
                                        <option value="0">Inactivo</option>
                                        <option value="1">Activo</option>
                                    </select>
                                    <script>
                                        document.ready = document.getElementById("ActClabe${cont}").value = "${clabe.Activo}"
                                    </script>
                                </td>
                                <td><input type="checkbox" id="Verificado${cont}" value="1" disabled>
                                    <script>
                                        if(${clabe.Verificado}){
                                            document.getElementById("Verificado${cont}").checked = true;
                                        }
                                    </script>
                                </td>
                                <td>
                                    <div style="display: block;">
                                        <button type="button" class="btn btn-primary admin-req" id="Editar_Aceptar${cont}" onclick="editar_aceptar(${cont})">Editar</button>
                                    </div>
                                </td>
                                <td>
                                    <div style="display: block;">
                                        <button type="button" class="btn btn-secondary" id="Cancelar${cont}" onclick="cancelar(${cont}, ${clabe.Activo})" style="display: none">Cancelar</button>
                                    </div>
                                </td>
                            </tr>
                        `;
                        cont++;
                        $("#TabClabes tbody").append(text);
                    });
                    
                }else{
                    $("#TabClabes tbody").empty();
                    $("#TabClabes").hide();
                    $("#EResultadoClabes").text("No se encontraron coincidencias.");
                }
            }
        });
    }else{
        $("#EResultadoClabes").text("Ingrese No. de empleado para buscar coincidencias.");
    }
}

function editar_aceptar(data){
    if ($("#Editar_Aceptar" + data).text() == "Editar") {

        $("#ActClabe" + data).attr("disabled", false);

        $("#Editar_Aceptar" + data).text("Aceptar");
        $("#Cancelar" + data).toggle();
    }
    else {
        guardar_modificar_clabe(data);
    }
}

function cancelar(data1, data2) {
    $("#ActClabe" + data1).attr("disabled", true);

    $("#ActClabe" + data1).val(data2);

    $("#Editar_Aceptar" + data1).text("Editar");
    $("#Cancelar" + data1).toggle();
}

function guardar_modificar_clabe(dato){
    var activos = $('select[id^=ActClabe]');
    console.log(activos);
    datos = {
        idPersona: $("#idPersona" + dato).val(),
        Clabe: $("#Clabe" + dato).val(),
        Activo: $("#ActClabe" + dato).val()
    };
    $.ajax({
        async: false,
        type: "POST",
        url: "/RH/modificarClabe",
        data: datos,
        success: function(data){
            if(data.encontrado){
                abrirModal("Información actualizada", "La información se actualizó de forma correcta.", "recargar");
            }else{
                abrirModal("Información no actualizada", "La información no se pudo actualizar.", "recargar");
            }
        }
    });
}