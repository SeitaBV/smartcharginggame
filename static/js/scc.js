$(document).ready(function() {

    /* game counters */

    $("#my_button_{{ i }}_{{ j }}").click(function() {
        $('#my_counter_{{ i }}_{{ j }}').html(function(i, val) { return +val+1 });
    });
});
