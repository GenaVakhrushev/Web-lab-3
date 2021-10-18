function create_task(){
    let title = document.getElementById("title").value;
    let description =  document.getElementById("description").value;

    fetch("/api/create_task",{
                            method:"POST",
                            body:JSON.stringify({"title":title,"description":description}),
                            headers:{"Content-Type":"application/json"}
                        }).then(response => {if(response.status == 200) location.reload();});
}

function delete_task(id){
    fetch("/api/delete_task", {
                            method:"POST",
                            body:JSON.stringify({"id":id}),
                            headers:{"Content-Type":"application/json"}
                        }).then(response => {if(response.status == 200) location.reload();});
}

function login(){
    let username = document.getElementById("username").value;
    let password =  document.getElementById("password").value;

    fetch("/api/check_pass",{
                            method:"POST",
                            body:JSON.stringify({"username":username,"password":password}),
                            headers:{"Content-Type":"application/json"}
                        }).then(response => {
                            if (response.redirected) {
                                window.location.href = response.url;
                            }
                            else if(response.status == 400)
                                document.getElementById("info").innerHTML = "Неправильные имя пользователя или пароль";
                            else if (response.status == 200)
                                return response.json();
                         })
}

function register(){
    let username = document.getElementById("username").value;
    let password =  document.getElementById("password").value;

    fetch("/api/register",{
                            method:"POST",
                            body:JSON.stringify({"username":username,"password":password}),
                            headers:{"Content-Type":"application/json"}
                        }).then(response => {
                            if (response.redirected) {
                                window.location.href = response.url;
                            }
                            else if(response.status == 400)
                                document.getElementById("info").innerHTML = "Такой пользователь уже существует";
                            else if (response.status == 200)
                                return response.json();
                         })
}