button_bind('#calibrate', 'cal')
button_bind('#session_start', 'session_start')
button_bind('#session_end', 'session_end')

function button_bind(button_id, socket_code) {
    $(function() {
        $(button_id).bind('click', function() {
            let call_url = '/socket_call?socket_code=' + socket_code;
            $.getJSON(call_url, function(data) {} );
            return false;
        });
    });
}