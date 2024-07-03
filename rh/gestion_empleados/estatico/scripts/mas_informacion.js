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

        $("#Idioma option").clone().appendTo(`#Idioma${cont}`);
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
                                <option value="0">-- Seleccione --</option>
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
        }
    })
});
