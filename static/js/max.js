$(document).on('click', ".add_uid", function () {
	let uid = $('#log_uid').val()
    $("#log_uid").val("");
    $.ajax({
        type: 'post',
        url: '/logic/add_uid',
        data: {add_uid: JSON.stringify(uid)},
        success: function (resp) {
            $(".status_logic").css("display", "inline-block");
            $('#total_add').replaceWith(resp.data);
            setTimeout(
              function() 
              {
                $(".status_logic").css("display", "none");
              }, 5000);
            }
      });

});
$(document).on('click', ".del_all", function () {
    $.ajax({
        type: 'post',
        url: '/logic/del_all',
        success: function (resp) {
            $(".status_logic").css("display", "inline-block");
            $('#total_add').replaceWith(resp.data);
            setTimeout(
              function() 
              {
                $(".status_logic").css("display", "none");
              }, 5000);
            }
      });

});

// Create request
var request = new XMLHttpRequest();
var interval = setInterval('update_status()',20000);

function update_status() {
if ( window.location.pathname == '/' ) {
request.open('GET', '/logic/check_status', true);
request.send(null);

request.onreadystatechange = function() {
    if (request.readyState == 4 && request.status == 200) {
        $('.status_uid').replaceWith(request.responseText);
        $.ajax({
          url: "/logic/qall_cookies",
          type: "GET",
          success: function (resp) {
              $('.reload_nick').replaceWith(resp.data);
          }
        });
    }}
}
}

$(document).on('click', ".add_nickfb", function () {
  let cookies = $('#log_uid').val()
    $("#log_uid").val("");
    $.ajax({
        type: 'post',
        url: '/logic/add_cookies',
        data: {add_cookies: JSON.stringify(cookies)},
        success: function (resp) {
            $.ajax({
                url: "/logic/qall_cookies",
                type: "GET",
                success: function (resp) {
                    $('.reload_nick').replaceWith(resp.data);
                }
                });
            $(".status_logic").css("display", "inline-block");
            $('#total_add').replaceWith(resp.data);
            setTimeout(
              function() 
              {
                $(".status_logic").css("display", "none");
              }, 5000);
            }
      });

});

$(document).on('click', ".delete_cookies", function () {
  let uid_nick = $(this).attr("id")
    $.ajax({
        type: 'post',
        url: '/logic/del_nick',
        data: {del_nick: JSON.stringify(uid_nick)},
        success: function (resp) {
                $.ajax({
                url: "/logic/qall_cookies",
                type: "GET",
                success: function (resp) {
                    $('.reload_nick').replaceWith(resp.data);
                }
                });
            }
      });

});

$(document).on('click',".checktoken", function(){
     $.ajax({
        type: 'GET',
        url: '/logic/check_token',
        success: function (resp) {
            $('#status_token').replaceWith(resp.data);
        }
    });
});

$(document).on('click',".update_token", function(){
    let token = $('#log_uid').val();
    $.ajax({
        type: 'post',
        url: '/logic/update_token',
        data: {token: token},
        success: function (resp) {
            if (resp == 'Done') {
                document.getElementById("log_uid").value = ""; 
            }
        }
    });
});
