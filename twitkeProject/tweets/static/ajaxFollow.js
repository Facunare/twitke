

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

function follow(e, btn){
    e.preventDefault();
    if(btn.id == 'button1'){

        followForm = new FormData(document.getElementById('followForm'));
    }else if(btn.id == "button2"){

        followForm = new FormData(document.getElementById('followForm2'));
    }else if(btn.id == "button3")
         followForm = new FormData(document.getElementById('followForm3'));

    var id = btn.getAttribute('tweet-id');
    
    fetch(`/follow/${id}`, {
        method: "POST",
        body: followForm,
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
        }
    }).then(function(res){
        return res.json();  // Convierte la respuesta a JSON
    }).then(function(data){
        
        
        if(btn.id == 'button1'){
            const cant_followers = document.querySelector('.cant_followers')
            if(data.is_follow){
                btn.querySelector('.followP').innerHTML = "Unfollow"
            }else{
                btn.querySelector('.followP').innerHTML = "Follow"
            }
    
            if(data.cant_followers == 1){
                cant_followers.innerHTML = data.cant_followers + "<span> seguidor</span>"
    
            }else{
                cant_followers.innerHTML = data.cant_followers + "<span> seguidores</span>"
            }

            
        }else if(btn.id == "button2"){

            if(data.is_follow){
                btn.querySelector('p').innerHTML = "Unfollow"
                btn.classList.add('unfollowButton')
                btn.classList.remove('follow')
            }else{
                btn.querySelector('p').innerHTML = "Follow"
                btn.classList.add('follow')
                btn.classList.remove('unfollowButton')
            }
        }else if(btn.id == "button3"){
            // if(data.is_follow){
            //     btn.querySelector('p').innerHTML = "Unfollow"
            //     btn.classList.add('unfollowButton')
            //     btn.classList.remove('follow')
            // }else{
            //     btn.querySelector('p').innerHTML = "Follow"
            //     btn.classList.add('follow')
            //     btn.classList.remove('unfollowButton')
            // } 
            location.reload()
        }
    }
        
    );
}
