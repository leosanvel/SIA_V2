$gmx(document).ready(function(){

    $("#btnCrearIdioma").on("click", function(){
        cont = 1;
        if ($(`#Columna${cont}`).length == 0){
            text = `<div class="row" id="Columna${cont}">
                    </div>`;
            $("#formularioMasInformacion").append(text);
        }
        text = `
            <div class="col-md-4">
                <div class="form-group">
                    <select id="Idioma${cont}" name="Idioma${cont}" class="opcional form-control">
                        <option value="0">-- Seleccione --</option>
                    </select>
                    <small id="EIdioma" class="etiquetaError form-text form-text-error"></small>
                </div>
            </div>
            <div class="col-md-2">
                <button type="button" class="btn btn-primary remover" id="RemoverIdioma${cont}">
                    <span class="bootstrap-icons" aria-hidden="true"><i class="bi bi-search"></i></span>
                    
                    </button>
            </div>
        `;
        $(`#Columna${cont}`).append(text);
    });

});
