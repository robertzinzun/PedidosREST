function incrementar(id){
    var cant="cant"+id;
    var exist="exis"+id;
    var cantidad=document.getElementById(cant).value;
    var existencia=parseInt(document.getElementById(exist).textContent);
    if(cantidad<existencia)
        cantidad++;
    else
        alert('Producto agotado');
    document.getElementById(cant).value=cantidad;
}
function decrementar(id){
    var cant="cant"+id;
    var cantidad=document.getElementById(cant).value;
    if(cantidad>1)
        cantidad--;
    document.getElementById(cant).value=cantidad;
}
function comprar(id){
    var cantAux="cant"+id;
    var precAux="prec"+id;
    var envio="envio"+id;
    var cantidad=parseInt(document.getElementById(cantAux).value);
    var precio=parseFloat(document.getElementById(precAux).textContent);
    var costoEnvio=parseFloat(document.getElementById(envio).textContent);
    document.getElementById("cantidad").textContent=cantidad;
    document.getElementById("precio").textContent=precio;
    document.getElementById("costoE").textContent=costoEnvio;
    document.getElementById("producto").textContent=document.getElementById("prod"+id).textContent;
    document.getElementById("subtotal").textContent=precio*cantidad;
    document.getElementById("subtotalE").textContent=costoEnvio*cantidad;
    document.getElementById("idProducto").value=id;
    document.getElementById("imagen").setAttribute("src","/productos/imagen/"+id);
    agregar();
}
function agregar(){
    var totalP=parseFloat(document.getElementById("totalP").value);
    var subtotal=parseFloat(document.getElementById("subtotal").textContent)
    var subtotalE=parseFloat(document.getElementById("subtotalE").textContent)
    document.getElementById("totalT").textContent=totalP+subtotal+subtotalE;
    var cantidad=parseInt(document.getElementById("cantidad").textContent)
    document.getElementById("cantidadP").value=cantidad;
}
function carrito(){
    var id=parseInt(document.getElementById("idProducto").value);
    var cantidad=parseInt(document.getElementById("cantidad").textContent);
    url="/pedidos/nuevo/"+id+"/"+cantidad;
    location.href=url;
}
