$gmx(document).ready(function(){
    $("#Quincena").change(cargar_info_crear_quincena);
    $("#btnCrearNomina").click(guardar_crear_nomina);
    $("#FechaPago").datepicker({
        dateFormat: 'dd/mm/yy',
        changeYear: true,
        changeMonth: true
    });
});

function cargar_info_crear_quincena(){
    if($("#Quincena").val()){
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/cargar-info-crear-nomina",
            data: {
                "idQuincena": $("#Quincena").val()
            },
            success: function(data){
                if(data){
                    FechaInicio = convertirFechaParaVisualizacion(data.FechaInicio);
                    FechaFin = convertirFechaParaVisualizacion(data.FechaFin);
                    anio = new Date(data.FechaInicio).getUTCFullYear();
                    var descripcion = 'NOMINA FEDERAL DE LA ' + data.Descripcion + ' DEL ' + anio;
                    var concepto = data.Descripcion + ' ' + anio;
                    var periodo = FechaInicio + ' AL ' + FechaFin;
                    $("#Descripcion").val(descripcion);
                    $("#ConceptoPago").val(concepto);
                    $("#Periodo").val(periodo);
                    $("#FechaInicio").val(FechaInicio);
                    $("#FechaFin").val(FechaFin);
                }
            }
        });
    }
}

function guardar_crear_nomina(event){
    event.preventDefault();
    if(validarFormulario($("#formularioCrearNomina")).valido){
        const formNomina = new FormData($("#formularioCrearNomina")[0]);
        formNomina.append("Usuario", $("#Usuario").text());
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/guardar-crear-nomina",
            data: formNomina,
            enctype: 'multipart/form-data',
            contentType: false,
            processData: false,
            success: function(data){
                if(data.guardado){
                    abrirModal("Nomina creada", "Los datos de la nómina han sido creados de manera correcta.", "recargar");
                }else{
                    abrirModal("Nomina ya existe", "Los datos de la nómina ya existen.", "recargar");
                }
            }
        });
    }
}

