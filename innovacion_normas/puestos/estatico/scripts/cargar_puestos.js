$gmx(document).ready(function(){
    $("#btnCargarArchivo").click(ProcesandoCargarPuestos);
});

function cargar_archivo(){
    window.document.getElementById("btnCargarArchivo").disabled = "";
    window.document.getElementById("Archivo").disabled = "";
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
            window.document.getElementById("ImgModal").style.display = "none";
            if(data.guardado){
                abrirModal("Datos cargados", "Los datos se han cargado correctamente.", "recargar");
            }else{
                abrirModal("Datos no cargados", "No se seleccionó un archivo.", "");
            }
        }
    });
}

function ProcesandoCargarPuestos(){
    //$("#GenerarArchivoNominaModal").modal('hide');
    //$("#btnDescargar").hide();
    window.document.getElementById("btnCargarArchivo").disabled = "disabled";
    window.document.getElementById("Archivo").disabled = "disabled";
    window.document.getElementById("ImgModal").style.display = "block";
    setTimeout(cargar_archivo, 2000);
}
