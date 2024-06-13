$gmx(document).ready(function(){
    $("#PuestoExistente").on("focus", function(){
        $("#lista_puestos").show();
    });

    $("#PuestoExistente").on("blur", function(event){
        if(!$(event.relatedTarget).closest("#lista_puestos").length){
            $("#lista_puestos").hide();
        }
    });

    $("#PuestoExistente").on("input", function(){
        var textoBusqueda = $(this).val();
        $.ajax({
            url: "/catalogos/actualizar-busqueda-puestos",
            method: "GET",
            data: {
                texto_busqueda: textoBusqueda
            },
            success: function(response){
                actualizarListaDesplegable(response);
            }
        })
    });

    $("#btnCargarArchivo").click(cargar_archivo);

});

function actualizarListaDesplegable(resultados){
    var listaDesplegable = $("#lista_puestos");
    listaDesplegable.empty(); // Vaciar la lista desplegable antes de agregar nuevos elementos
    resultados.forEach(function(resultado){
        var nuevoElemento = $('<div>', {
            'class': 'dropdown-item form-group',
            'html': $('<a>', {
                'href': 'javascript:void(0)', // El href está configurado para evitar que la página se recargue
                'data-id': resultado.ConsPuesto,
                'data-texto': resultado.Puesto,
                'text': resultado.Puesto,
                'click': function(){
                    var textoSeleccionado = $(this).data('texto');
                    $("#PuestoExistente").val(textoSeleccionado);
                    $("#lista_puestos").hide();
                }
            })
        });
        listaDesplegable.append(nuevoElemento);
    });
}

function cargar_archivo(){
    const archivo = new FormData();
    archivo.append('archivo', $("#Archivo")[0].files[0]);

    console.log(archivo);

    $.ajax({
        async: false,
        type: "POST",
        url: "/catalogos/cargar_archivo_puestos",
        data: archivo,
        enctype: "multipart/form-data",
        contentType: false,
        processData: false,
        success: function(data){
            if(data.guardado){
                abrirModal("Datos cargados", "Los datos se han cargado correctamente.", "recargar");
            }
        }
    });
}