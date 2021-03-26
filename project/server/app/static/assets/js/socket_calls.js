$(function() {
    $('a#calibrate').bind('click', function() {
      $.getJSON('/socket_call?socket_code=cal',
        function(data) {
      });
      return false;
    });
  });

$(function() {
$('a#session_start').bind('click', function() {
    $.getJSON('/socket_call?socket_code=session_start',
    function(data) {
        console.log("start");
    });
    return false;
});
});

$(function() {
$('a#session_end').bind('click', function() {
    $.getJSON('/socket_call?socket_code=session_end',
    function(data) {
    });
    return false;
});
});