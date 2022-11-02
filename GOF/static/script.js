function validateform(){
    var form = document.forms['myForm'];
    var uname = form['username'].value;
    var fname = form['firstname'].value;
    var lname = form['lastname'].value;
    var number = form['phonenumber'].value;
    var occupation = form['occupation'].value;
    var college = form['college'].value;
    var pass = form['password'].value;
    var pass1 = form['password1'].value;
    var retval = true;
    let reg_al = /[a-zA-Z]{1}/;
    let reg_num = /[0-9]{1}/;
    let reg_spc = /[!@#$%^&*?]{1}/;
    let reg_phonenumber = /[+]{1}[0-9]{2}[0-9]{10}/;
    
    //username
    if(uname.length<=5 || !reg_al.test(uname) || !reg_num.test(uname) || !reg_spc.test(uname))
    {
        retval = false;
        element = document.getElementById('uname');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Username must have more than 5 charecters !<br>Username must contains alphabates !<br>Username must contains numbers !<br>Username must contains spacial characters !";
    }

    //phonenumber
    if(!reg_phonenumber.test(number))
    {
        retval = false;
        element = document.getElementById('pnum');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Mobile numbers contains extact 10 digits !<br> Please enter mobile number with country code !";
    }

    //password
    if(uname.length<8 || !reg_al.test(pass) || !reg_num.test(pass) || !reg_spc.test(pass))
    {
        retval = false;
        element = document.getElementById('pass');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Password must have more than 8 charecters !<br>Password must contains alphabates !<br>Password must contains digits !<br>Password must contains spacial characters !";
    }

    //password1 pass1
    if(pass.localeCompare(pass1) == 1)
    {
        retval = false;
        element = document.getElementById('pass1');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Passwords doesn't matched";
    }

    //fname fname
    if(!reg_al.test(fname))
    {
        retval = false;
        element = document.getElementById('fname');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Enter proper first name";
    }

    //lname lname
    if(!reg_al.test(lname))
    {
        retval = false;
        element = document.getElementById('lname');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Enter proper last name";
    }

    //college col
    if(!reg_al.test(college))
    {
        retval = false;
        element = document.getElementById('col');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Enter proper college name";
    }

    //occupation occ
    if(!reg_al.test(occupation))
    {
        retval = false;
        element = document.getElementById('occ');
        element.getElementsByClassName('invalid-feedback')[0].innerHTML = "Enter proper occupation";
    }

    return retval;
}


function preview_ans_fun() {
    console.log("clicked");
    let text = document.getElementById("ans_field").value;
    console.log("text ", text);
    text = text.replace(/#/g, "`");
    text = text.replace(/\n/g, "~");
    console.log("final-text ", text);
    const xhr = new XMLHttpRequest();
    xhr.open("GET", '/xhrreq/'+text, true);
    xhr.onload = function () {
        if(this.status === 200){
            document.getElementById("prv_ans_field").innerHTML = this.responseText;
        }
        else{
            console.log("Some error occured")
        }
    }
    xhr.send();
}


function preview_que_fun() {
    console.log("clicked");
    let text = document.getElementById("que_field").value;
    const xhr = new XMLHttpRequest();
    xhr.open("POST", '/xhrreq', true);
    xhr.getResponseHeader('content-type', 'text');

    xhr.onload = function () {
        if(this.status === 200){
            document.getElementById("prv_que_field").innerHTML = this.responseText;
        }
        else{
            console.log("Some error occured");
        }
    }
    xhr.send(text);
}


function fetch_like(que_id){
    console.log('fetch_like');
    const xhr = new XMLHttpRequest();
}

function like(id, n){
    console.log('increment_like', id , n);
    const xhr = new XMLHttpRequest();
    if(n==-1){
        xhr.open("GET", '/xhrincrement/que/'+id, true);
    }
    else if(n==1){
        xhr.open("GET", '/xhrincrement/comment/'+id, true);
    }
    xhr.onload = function () {
        if(this.status === 200){
            if(this.responseText.localeCompare("-1")!=0)
                document.getElementById("likes"+id).innerHTML = this.responseText;
            else
                alert("you already liked this content");
        }
        else{
            console.log("Some error occured");
        }
    }
    xhr.send();
}


function display(file) {
    const myWindow = window.open();
    myWindow.document.open();
    myWindow.document.write(file);
    myWindow.document.close();
  }