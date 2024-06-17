$gmx(document).ready(function(){
    $("#btnCargarArchivo").click(cargar_archivo);
});

function cargar_archivo(){
    const archivo = new FormData();
    archivo.append("archivo", $("#Archivo")[0].files[0]);

    $.ajax({
        async: false,
        type: "POST",
        url: "/innovacion-normas/puestos/cargar-archivo-puestos",
        data: archivo,
        enctype: "multipart/form-data",
        contentType: false,
        processData: false,
        success: function(data){
            if(data.guardado){
                abrirModal("Datos cargados", "Los datos se han cargado correctamente.", "recargar");
            }else{
                abrirModal("Datos no cargados", "No se seleccionó un archivo.", "");
            }
        }
    });
}