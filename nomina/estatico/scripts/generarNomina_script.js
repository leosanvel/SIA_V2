
function generarNomina() {
    console.log("GENERANDO NÓMINA")
    $.ajax({
        async: false,
        type: "POST",
        url: "/Nomina/crearNomina",
        data: $("#formularioGenerarNomina").serialize(),
        success: function (data) {
            console.log("TERMINADO")
        }
    });
}