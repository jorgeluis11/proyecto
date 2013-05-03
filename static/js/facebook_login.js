window.fbAsyncInit = function() {
          FB.init({
            appId      : '427075444041786',
            status     : true, 
            cookie     : true,
            xfbml      : true,
            oauth      : true,
          });
          FB.getLoginStatus(function(response) {
          if (response.status === 'connected') {
            login();
          } else if (response.status === 'not_authorized') {
            // not_authorized
          } else {
            // not_logged_in
          }
         });
        };
        (function(d){
           var js, id = 'facebook-jssdk'; if (d.getElementById(id)) {return;}
           js = d.createElement('script'); js.id = id; js.async = true;
           js.src = "//connect.facebook.net/en_US/all.js";
           d.getElementsByTagName('head')[0].appendChild(js);
         }(document));


       function login() {
    FB.login(function(response) {
        if (response.authResponse) {
            // connected
            testAPI();
        } else {
            // cancelled
        }
    });
}

     function testAPI() {
    FB.api('/me', function(response) {
        
        alert(response.id)
        $.post("register_login", 
          { 
            id: response.id,
            name: response.name,
            first_name: response.first_name,
            last_name: response.last_name,
            email: response.email,
            gender: response.gender,
            'csrfmiddlewaretoken': '{{ csrf_token }}'

          },
           function(data) 
           {
            location.reload()
           });
    });
}