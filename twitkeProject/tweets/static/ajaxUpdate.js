
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function update(e, btn){
    e.preventDefault();
    var updateForm = new FormData(document.getElementById('updateForm'));
    var id = btn.getAttribute('tweet-id');
    console.log(id)
    fetch(`../update/profiles/${id}`, {
        method: "POST",
        body: updateForm,
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        const error = document.querySelector('.error')
        console.log(data)
        if(data.is_used){
            error.innerHTML = "Ese nombre ya esta en uso"
        }
    })
}