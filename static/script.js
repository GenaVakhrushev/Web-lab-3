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