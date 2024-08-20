$gmx(document).ready(function(){

    $("#btnCrearIdioma").on("click", function(){
        var cont = $(".idioma").length + 1;
        text = `
            <div class="row fila-idioma">
                <div class="col-md-8">
                    <div class="form-group">
                        <select id="Idioma${cont}" name="Idioma${cont}" class="opcional form-control idioma">
                            
                        </select>
                        <small id="EIdioma${cont}" class="etiquetaError form-text form-text-error"></small>
                    </div>
                </div>
                <div class="col-md-2">
                    <button type="button" class="btn btn-primary btn-sm remover" id="RemoverIdioma${cont}">
                        <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                    </button>
                </div>
            </div>
        `;
        $(`#ColIdiomas`).append(text);

        $("#Idioma1 option").clone().appendTo(`#Idioma${cont}`);
    });

    $(document).on("click", ".remover", function(){
        $(this).parents(".fila-idioma").remove();
    });

    $("#btnCrearIdiomaIndigena").on("click", function(){
        if($("#Indigena").val() == "1"){
            var cont = $(".indigena").length + 1;
            text = `
                <div class="row fila-idioma">
                    <div class="col-md-8">
                        <div class="form-group">
                            <select id="IdiomaIndigena${cont}" name="IdiomaIndigena${cont}" class="opcional form-control indigena">
                                
                            </select>
                            <small id="EIdiomaIndigena${cont}" class="etiquetaError form-text form-text-error"></small>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <button type="button" class="btn btn-primary btn-sm remover" id="RemoverIdiomaIndigena${cont}">
                            <span class="glyphicon glyphicon-remove" aria-hidden="true"></span>
                        </button>
                    </div>
                </div>
            `;
            $("#ColIdiomasIndigenas").append(text);

            $("#LenguaIndigena option").clone().appendTo(`#IdiomaIndigena${cont}`);
        }
    });

    $("#btnAgregarIdioma").click(mostrarFilaAgregarIdioma);
    $("#btnOcultarFilaAgregarIdioma").click(ocultarFilaAgregarIdioma);

    $("#btnAgregarIndigena").click(mostrarFilaAgregarIndigena);
    $("#btnOcultarFilaAgregarIndigena").click(ocultarFilaAgregarIndigena);

    $("#btnGuardarIdioma").click(guardarIdioma);
    $("#btnGuardarIndigena").click(guardarIndigena);
});

function mostrarFilaAgregarIdioma(){
    $("#FilaAgregarIdioma").show();
    $("#AgregarIdioma").prop("disabled", false);
}

function ocultarFilaAgregarIdioma(){
    $("#FilaAgregarIdioma").hide();
    $("#AgregarIdioma").val("");
    $("#AgregarIdioma").prop("disabled", true);
    $("#EAgregarIdioma").text("");
}

function mostrarFilaAgregarIndigena(){
    $("#FilaAgregarIndigena").show();
    $("#AgregarIndigena").prop("disabled", false);
}

function ocultarFilaAgregarIndigena(){
    $("#FilaAgregarIndigena").hide();
    $("#AgregarIndigena").val("");
    $("#AgregarIndigena").prop("disabled", true);
    $("#EAgregarIndigena").text("");
}

function guardarIdioma(){
    if($("#AgregarIdioma").val() != ""){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/guardar-idioma",
            data: {
                NuevoIdioma: $("#AgregarIdioma").val()
            },
            success: function(data){
                if(data){
                    if(data.guardado){
                        abrirModal("Idioma guardado", "El idioma se agregó correctamente.", "");
                        obtenerIdiomas(data.idIdioma);
                    }else{
                        abrirModal("Idioma no guardado", "El idioma ya existe.", "");
                    }
                }
            }
        });
    }else{
        $("#EAgregarIdioma").text("Campo vacío.");
    }
}

function obtenerIdiomas(Idioma){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/obtener-idiomas",
        success: function(data){
            if(data){
                $(".idioma").each(function(){
                    val_aux = $(this).val();
                    $(this).find("option").remove();
                    $(this).html(data);
                    if(val_aux == 0){
                        $(this).val(Idioma);
                    }else{
                        $(this).val(val_aux);
                    }
                });
                $("#FilaAgregarIdioma").hide();
                $("#AgregarIdioma").val("");
                $("#AgregarIdioma").prop("disabled", true);
            }
        }
    });
}

function guardarIndigena(){
    if($("#AgregarIndigena").val() != ""){
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-empleados/guardar-indigena",
            data: {
                NuevoIndigena: $("#AgregarIndigena").val()
            },
            success: function(data){
                if(data){
                    if(data.guardado){
                        abrirModal("Lengua indigena guardada", "La lengua indigena se agregó correctamente.", "");
                        obtenerLenguasIndigenas(data.idLenguaIndigena);
                    }else{
                        abrirModal("Lengua indigena no guardada", "La lengua indigena ya existe.", "");
                    }
                }
            }
        });
    }else{
        $("#EAgregarIndigena").text("Campo vacío.");
    }
}

function obtenerLenguasIndigenas(idLenguaIndigena){
    $.ajax({
        async: false,
        type: "POST",
        url: "/rh/gestion-empleados/obtener-lenguas-indigenas",
        success: function(data){
            if(data){
                $(".indigena").each(function(){
                    val_aux = $(this).val();
                    $(this).find("option").remove();
                    $(this).html(data);
                    if(val_aux == 0){
                        $(this).val(idLenguaIndigena);
                    }else{
                        $(this).val(val_aux);
                    }
                });
                $("#FilaAgregarIndigena").hide();
                $("#AgregarIndigena").val("");
                $("#AgregarIndigena").prop("disabled", true);
            }
        }
    });
}