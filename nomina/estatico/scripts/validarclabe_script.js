$gmx(document).ready(function(){
    $("#btnBuscaClabe").click(obtener_clabe);
    //$("#btnVerificarModal").click(abrirAdModal);
    $("#btnVerificarClabe").click(verificar_clabe);
    obtener_clabe_masivo();
});

function mostrar_btn_buscar(){
    if($("#NumeroBuscarEmpleado").val() != ""){
        $("#btnBuscaClabe").show();
        console.log($("#NumeroBuscaEmpleado").val());
    }else{
        $("#btnBuscaClabe").hide();
        console.log($("#NumeroBuscaEmpleado").val());
    }
}

function obtener_clabe(event){
    if($("#NumeroBuscarEmpleado").val() != ""){
        $.ajax({
            async: false,
            type: "POST",
            url: "/Nomina/buscarClabe",
            data: {
                "idPersona": $("#idPersona").val()
            },
            success: function(data){
                if(data){
                    if(data.encontrado == false){
                        abrirModal("Clabe no encontrada", "El empleado no tiene una clabe interbancaria guardada.", "recargar")
                    }else if(data.verificado){
                        abrirModal("Clabe ya verificada", "La clabe interbancaria ya ha sido verificada.", "recargar")
                    }else{
                        $("#resultado").show();
                        $("#Clabe").val(data.Clabe);
                        $("#Banco").val(data.Banco);
                        $("#btnDescargarEdoCuenta").wrap('<a href="' + data.url_descarga + '"download></a>');
                    }
                }
            }
        })
    }
}

function abrirAdModal(dato){
    if(dato == ""){
        if(validarFormulario($("#formularioValidarClabe")).valido){
            $("#MensajeAdModal").html("¿Esta seguro de validar la clabe " + $("#Clabe").val() + " para el empleado " + $("#NumeroBuscarEmpleado").val()  + "?");
            $("#AsegurarVerificarModal").modal('show');
        }
    }else{
        $("#MensajeAdModal").html("¿Esta seguro de validar la clabe " + $("#clabe" + dato).val() + " para el empleado " + $("#idPersona" + dato).val()  + "?");
        $("#AsegurarVerificarModal").modal('show');
    }
    $("#dato").val(dato);
}

function verificar_clabe(){
    var dato = $("#dato").val();
    console.log(dato);
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/verificarClabe",
        data: {
            "idPersona": $("#idPersona" + dato).val(),
            "Clabe": $("#Clabe" + dato).val()
        },
        success: function(data){
            if(data.verificado){
                abrirModal("Verificación correcta", "Se ha verificado de forma correcta la clabe interbancaria.", "recargar");
            }else{
                abrirModal("Verificación incorrecta", "No se ha podido verificar la clabe interbancaria.", "recargar");
            }
        }
    });
}

function obtener_clabe_masivo(){
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/buscarClaveMasivo",
        success: function(data){
            if(data){
                console.log(data);
                if(data.resultado == false){
                    abrirModal("Verificación incorrecta", "No se ha podido verificar la clabe interbancaria.", "recargar");
                }else{
                    $("#TabMasivoClabe").show();
                    $("#TabMasivoClabe tbody").empty();
                    var cont = 1;
                    data.forEach(function(clabe){
                        text = `
                        <tr>
                            <td><input class="form-control" type="text" id="idPersona${cont}" value="${clabe.idPersona}" readonly></input></td>
                            <td><input class="form-control" type="text" id="Clabe${cont}" value="${clabe.Clabe}" readonly></input></td>
                            <td><input class="form-control" type="text" id="Banco${cont}" value="${clabe.Banco}" readonly></input></td>
                            <td>
                                <select id="ActClabe${cont}" name="ActClabe${cont}" class="form-control" value="${clabe.Activo}" disabled>
                                    <option value="0">Inactivo</option>
                                    <option value="1">Activo</option>
                                </select>
                                <script>
                                    document.ready = document.getElementById("ActClabe${cont}").value = "${clabe.Activo}"
                                </script>
                            </td>
                            <td>
                                <input type="checkbox" id="Verificado${cont}" value="1" disabled>
                                <script>
                                    if(${clabe.Verificado}){
                                        document.getElementById("Verificado${cont}").checked = true;
                                    }
                                </script>
                            </td>
                            <td>
                                <div style="display: block;">
                                    <button type="button" id="EdoCuenta${cont}")"><img src="/nomina/static/image/PDF_file_icon.png" height="25" width="20"/></button>
                                </div>
                            </td>
                            <td>
                                <div style="display: block;">
                                    <button type="button" class="btn btn-primary" id="Verificar${cont}" onclick="abrirAdModal(${cont})">Verificar</button>
                                </div>
                            </td>
                        </tr>
                        `;
                        $("#TabMasivoClabe tbody").append(text);
                        $("#EdoCuenta" + cont).wrap('<a href="' + clabe.url_descarga + '"download></a>');
                        cont++;
                    }); 
                }
            }
        }
    });
}