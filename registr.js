function div_show() {
    document.getElementById('loginwraper').style.display = "block";
    }
    
    function div_hide(){
    document.getElementById('loginwraper').style.display = "none";
    }
    
    function store(){
    event.preventDefault();
    
    var name = document.getElementById('name');
    var email = document.getElementById('email');
    var regexEmail = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    var pw1 = document.getElementById('pw1');
    var pw2 = document.getElementById('pw2');
    
    if(email.value.length == 0){
        document.getElementById('errEmail').innerHTML='Please fill in email';
      
    }else if(!regexEmail.test(email.value)){
        document.getElementById('errEmail').innerHTML='Please provide a valid email address';
    }
    else if(name.value.length == 0){
        document.getElementById('errName').innerHTML='Please fill in your name';
    
    }else if(pw1.value.length == 0){
        document.getElementById('errPw1').innerHTML='Please fill in password';
    
    }else if(email.value.length == 0 && name.value.length == 0 && pw1.value.length == 0){
        document.getElementById('errGen').innerHTML='Please fill in your name, email and password';
    
    }else if(pw1.value != pw2.value){
        document.getElementById('errPw2').innerHTML='Please check the password';
    
    }else{
        localStorage.setItem('name', name.value);
        localStorage.setItem('email', email.value);
        localStorage.setItem('pw1', pw1.value);
        document.getElementById('status').innerHTML='Your account has been created';
        document.getElementById('errEmail').innerHTML='';
        document.getElementById('errName').innerHTML='';
        document.getElementById('errPw1').innerHTML='';
        document.getElementById('errPw2').innerHTML='';
        document.getElementById('errGen').innerHTML='';
    }
    
    var i;
    
    console.log("local storage");
    for (i = 0; i < localStorage.length; i++)   {
        console.log(localStorage.key(i) + "=[" + localStorage.getItem(localStorage.key(i)) + "]");
    }
    }
    