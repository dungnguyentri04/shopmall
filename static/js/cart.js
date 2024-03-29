let updateBtn = document.getElementsByClassName("update-cart")
for (i=0;i<updateBtn.length;i++){
    updateBtn[i].addEventListener("click",function(){
        event.preventDefault()
        let quantity,color,size
        if (this.classList.contains("add_cart_btn")){
            quantity =  parseInt(document.getElementById("value_quantity").value)
            let select_color = document.getElementById("form-select-color")
            let select_size = document.getElementById("form-select-size")
            color = select_color.options[select_color.selectedIndex].value
            size = select_size.options[select_size.selectedIndex].value
        }
        else {
            quantity = 1
            color = this.dataset.color
            size = this.dataset.size
        }
        let varient = {"size":size,"color":color}
        let productId = this.dataset.product
        let action = this.dataset.action
        if (user=="AnonymousUser"){
            addCookieItem(productId,action,quantity,varient)
        }
        else{
            updateUserOrder(productId,action,quantity,varient)
        }
    })
}


function updateUserOrder(productId,action,quantity,varient){
    const url = "/update_item/"
    fetch(url,{
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({"productId":productId,"action":action,"quantity":quantity,"varient":varient})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log("data:", data);
        location.reload()
        })
}


function addCookieItem(productId,action,quantity,varient){
    // console.log("not login")
    let product = productId + "_" + varient.color + "_" + varient.size
    if (action == 'add'){
        if (cart[product] == undefined){
            cart[product] = {"quantity":quantity}
        }
        else {
            cart[product]["quantity"]+=quantity;
        }
    }
    else if (action == "remove"){
        cart[product]["quantity"] -= 1
        if (cart[product]["quantity"] <= 0 ){
            delete cart[product]
        }
    }
    else if (action == "delete"){
        delete cart[product]
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}
