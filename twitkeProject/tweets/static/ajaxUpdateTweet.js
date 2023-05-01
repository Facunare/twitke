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

function edit(e, btn, type){
    e.preventDefault();
    var id = btn.getAttribute('tweet-id');
    
    if(type == "GET"){
      const buttonSave = document.querySelector('.update')
      buttonSave.id = id
      fetch(`../update/tweet/${id}`, {
        method: "GET",
        headers: {
          "X-CSRFToken": getCookie('csrftoken'),
          "X-Requested-With": "XMLHttpRequest"
        }
      }).then(function(res){
        return res.json()
      }).then(function(data){
        const textarea = document.getElementById('textArea');
        textarea.value = data.tweetContent;

      });
    }else if(type == "POST"){
      const buttonSave = document.querySelector('.update')
      var updateTweetForm = new FormData(document.getElementById('updateTweetForm'));
      tweetId = buttonSave.id
      fetch(`../update/tweet/${tweetId}`, {
        method: "POST",
        body: updateTweetForm,
        headers: {
          "X-CSRFToken": getCookie('csrftoken'),
          "X-Requested-With": "XMLHttpRequest"
        }
      }).then(function(res){
          return res.json()
      }).then(function(data){
          location.reload()
      })

    }
  }