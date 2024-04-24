function actualizar(estatus){
    var idPedido=document.getElementById('idPedido').value;
    var idTarjeta=document.getElementById('idTarjeta').value;
    var valoracion=document.getElementById('valoracion');
    if(valoracion!=null){
        valoracion=valoracion.value;
    }
    var datos={idPedido:idPedido,
               idTarjeta:idTarjeta,
               valoracion:valoracion,
               estatus:estatus
              };
    url='/pedidos/modificar';
    var ajax=new XMLHttpRequest();
    ajax.open("post",url,true);
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            var respuesta=JSON.parse(this.responseText);
            //alert(respuesta.mensaje);
            location.href='/pedidos/ver/'+idPedido;
        }
    }
    ajax.setRequestHeader("Content-type", "application/json");
    ajax.send(JSON.stringify(datos));
}
function valorar(valor){
    document.getElementById('valoracion').value=valor;
    var valoracion=document.getElementById('valoracion').value;
    document.getElementById('valoracionL').textContent=valor;
}