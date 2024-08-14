$gmx(document).ready(function () {


    $("#btnGuardaPoliticaPersona").click(function (event) {

        var formData = {
            idPersona: $("#idPersona").val(),
            checkboxesData: {}
        };

        // Iterar sobre los checkboxes y agregar al objeto si están marcados
        $("input[type=checkbox]").each(function () {
            var checkboxId = this.id.match(/\d+/);
            formData.checkboxesData[checkboxId] = this.checked;
        });
        console.log("formData");
        console.log(formData);

        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/guarda-politicas-persona",
            contentType: "application/json",
            data: JSON.stringify(formData),
            success: function (data) {
                if (data) {
                    abrirModal("Información guardada", "Las políticas se actualizaron con éxito", "");
                }
            }
        });

    });

    $("#btnBuscaPolitica").click(function (event) {
        event.preventDefault();
        BuscaPolitica();
    });

});

function funcionSeleccionar() { //se ejecuta al seleccionar el empleado en el modal
    BuscaPolitica();
}

function BuscaPolitica(){
    if (validarFormulario($("#formularioBuscaPolitica")).valido) {
        $.ajax({
            async: false,
            type: "POST",
            url: "/rh/gestion-asistencias/buscar-politica",
            data: $("#formularioBuscaPolitica, #idPersona").serialize(),
            success: function (data) {
                if(data.respuesta == "1"){                                    
                    $("#EResultado").text("");
                    // Limpiar la tabla existente
                    $("#tablaResultadosPolitica tbody").empty();

                    $("#tablaResultadosPolitica").show();

                    $("#btnGuardaPoliticaPersona").show();

                    // Iterar sobre los elementos
                    data.politicas.forEach(function (politica) {
                        $("#tablaResultadosPolitica tbody").append(`
                        <tr>  
                            <td>${politica.idPolitica}</td>  
                            <td>${politica.Politica}</td>  
                            <td><input type="checkbox" id="check${politica.idPolitica}" class="desactiva-empleado"></td>  
                        </tr>
                        `);
                    });

                    // Iterar sobre los elementos
                    data.politicas_persona.forEach(function (politica_persona) {
                        $(`#check${politica_persona.idPolitica}`).prop("checked", true);
                    });
                }else{
                    abrirModal("Politicas", "Las políticas solo son para personal de plaza", "recargar");                   
                }
            }
        });
    }
}