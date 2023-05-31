

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

function retweet(e, btn){
    e.preventDefault();
    var retweetForm = new FormData(document.getElementById('retweetForm'));
    var id = btn.getAttribute('tweet-id');

    fetch(`../retweet/${id}`, {
        method: "POST",
        body: retweetForm,
        headers: {
            "X-CSRFToken": getCookie('csrftoken'),
            "X-Requested-With": "XMLHttpRequest"
        }
    }).then(function(res){
        return res.json()
    }).then(function(data){
        console.log(data)
        if (data.is_retwitted) {
            btn.querySelector('.retweetSvg').setAttribute('fill', 'green');
           if(data.darkMode){
            btn.querySelector('.retweetSvg path:last-child').setAttribute('fill', 'green');
           }
        } else {
            btn.querySelector('.retweetSvg').removeAttribute('fill');
          
            btn.querySelector('.retweetSvg path:last-child').removeAttribute('fill');
               
    
            
        }        
        const rts = document.querySelectorAll('.retweetCount')
        
        for(let rt of rts){
            console.log(rt)
            if (rt.id == data.id) {
                if (data.retweets === 0) {
                    rt.innerHTML = '';
                } else {
                    rt.innerHTML = data.retweets;
                }
            }
        }
    })
}