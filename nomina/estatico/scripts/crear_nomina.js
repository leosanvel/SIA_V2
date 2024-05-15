$gmx(document).ready(function(){
    $("#Quincena").change(cargar_info_crear_quincena);
    $("#btnCrearNomina").click(guardar_crear_nomina);
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
                }
            }
        });
    }
}

function guardar_crear_nomina(event){
    event.preventDefault();
    if(validarFormulario($("#formularioCrearNomina")).valido){
        $.ajax({
            async: false,
            type: "POST",
            url: "/nomina/guardar-crear-nomina",
            data: $("#formularioCrearNomina").serialize(),
            success: function(data){
                if(data){

                }
            }
        });
    }
}