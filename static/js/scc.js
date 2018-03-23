
// Shortcuts

$(document).keydown(function(e) {

    // Move to next on Enter
    if (e.which == 13) {
        console.log("Enter key pressed - clicking next move.");
        $("#next_turn").click();
    }

    // Station 1
    if (e.which == 48 + 1) {
        console.log("Shortcut for charging car 1.");
        var btn = $('#add_one_ChargingStation0');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }
    if (e.which == 48 + 1 + 4) {
        console.log("Shortut for discharging car 1.");
        var btn = $('#remove_one_ChargingStation0');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }

    // Station 2
    if (e.which == 48 + 2) {
        console.log("Shortcut for charging car 2.");
        var btn = $('#add_one_ChargingStation1');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }
    if (e.which == 48 + 2 + 4) {
        console.log("Shortut for discharging car 2.");
        var btn = $('#remove_one_ChargingStation1');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }

    // Station 3
    if (e.which == 48 + 3) {
        console.log("Shortcut for charging car 3.");
        var btn = $('#add_one_ChargingStation2');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }
    if (e.which == 48 + 3 + 4) {
        console.log("Shortut for discharging car 3.");
        var btn = $('#remove_one_ChargingStation2');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }

    // Station 4
    if (e.which == 48 + 4) {
        console.log("Shortcut for charging car 4.");
        var btn = $('#add_one_ChargingStation3');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }
    if (e.which == 48 + 4 + 4) {
        console.log("Shortut for discharging car 4.");
        var btn = $('#remove_one_ChargingStation3');
        if (btn && !btn.prop('disabled')) {
            btn.click();
        }
    }
});
