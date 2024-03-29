
validator = function(obj){
    function validate(inputElement,ruleElement){
        let errorElement = inputElement.parentElement.querySelector(obj.errorSelector)
        inputElement.onblur = function(){
            // console.log("check")
            let inputEmail = ruleElement.checkEmail(inputElement.value)
            let errorMessage = ruleElement.test(inputElement.value)
            let inputPassword = ruleElement.minLength(inputElement.value)
            let inputConfirmPassword = ruleElement.checkConfirm(inputElement.value)
            if (errorMessage){
                errorElement.innerText = errorMessage
                inputElement.parentElement.classList.add("invalid")
                inputElement.parentElement.classList.remove("valid")
            }
            else if (inputEmail){
                errorElement.innerText = inputEmail
                inputElement.parentElement.classList.add("invalid")
                inputElement.parentElement.classList.remove("valid")
                }
            else if (inputPassword){
                errorElement.innerText = inputPassword
                inputElement.parentElement.classList.add("invalid")
                inputElement.parentElement.classList.remove("valid")
                }
            else if (inputConfirmPassword){
                errorElement.innerText = inputConfirmPassword
                inputElement.parentElement.classList.add("invalid")
                inputElement.parentElement.classList.remove("valid")
            }
            else { 
                errorElement.innerText = "Valid"
                inputElement.parentElement.classList.remove("invalid")
                inputElement.parentElement.classList.add("valid")
            }
        }
    }


    let formElement = document.querySelector(obj.form)
    if (formElement){
        obj.rules.forEach(ruleElement => {
            // console.log(ruleElement)
            let inputElement = form.querySelector(ruleElement.select)
            if (inputElement){
                validate(inputElement,ruleElement)
            }
            inputElement.oninput = function(){
                let errorElement = inputElement.parentElement.querySelector(obj.errorSelector)
                errorElement.innerText = ""
                inputElement.parentElement.classList.remove("invalid")
            }
        });
    }


}

validator.isRequired = function(select){
    return {
        select: select,
        test: function(text){
            return text.trim() ? undefined : "You have not entered text"
        },
        checkEmail: function (text){
        },
        minLength: function (text){
        },
        checkConfirm: function (text){
        },
    }
}

validator.isEmail = function(select){
    return {
        select: select,
        test: function(text){
            return text.trim() ? undefined : "You have not entered text"
        },
        checkEmail: function(text){
            let regax = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
            return regax.test(text.trim()) ? undefined : "This must be a gmail"
        },
        minLength: function (text){
        },
        checkConfirm: function (text){
        },
    }
}

validator.isPassword = function(select){
    return {
        select: select,
        test: function(text){
            return text.trim() ? undefined : "You have not entered text"
        },
        checkEmail: function (text){
        },
        minLength: function (text){
            return text.length >=6 ? undefined : "The minlength must be more than 6"
        },
        checkConfirm: function (text){
        },
        
    }
}


validator.confirmPassword = function(select,confirmValue){
    return {
        select: select,
        test: function(text){
            return text.trim() ? undefined : "You have not entered text"
        },
        checkConfirm : function(text){
            return text === confirmValue() ? undefined : "Your password is wrong"
        },
        checkEmail: function (text){
        },
        minLength: function (text){
        },
    }
}


