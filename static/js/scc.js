
// Shortcuts

var keysDown = {};

var enterKeyCode = 13;
var cKeyCode = 67;
var dKeyCode = 68;
var oneKeyCode = 49;
var escKeyCode = 27;
var shiftKeyCode = 16;
var nKeyCode = 78;
var rKeyCode = 82;

$(document).keydown(function (e) {
    keysDown[e.which] = true;
    keysDown[shiftKeyCode] = e.shiftKey;
    executeShortCuts();
});

$(document).keyup(function (e) {
    delete keysDown[e.which];
    executeShortCuts();
});

function executeShortCuts() {

    // Reset game on Shift+R
    if (rKeyCode in keysDown && keysDown[shiftKeyCode] == true) {
        console.log("Shift+r pressed - clicking reset game.");
        $("#reset_game").click();
    }

    // New game on Shift+N
    if (nKeyCode in keysDown && keysDown[shiftKeyCode] == true) {
        console.log("Shift+n pressed - clicking new game.");
        $("#new_game").click();
    }

    // Move to next on Enter
    if (enterKeyCode in keysDown) {
        console.log("Enter key pressed - clicking next turn.");
        $("#next_turn").click();
    }

    // Close dialog
    if (escKeyCode in keysDown) {
        console.log("Escape key pressed - closing dialog.");
        $('.alert').alert('close');
    }

    // Station 1
    if (oneKeyCode in keysDown){
        if (cKeyCode in keysDown) {
            console.log("Shortcut for charging car at station 1.");
            var btn = $('#add_one_ChargingStation0');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
        if (dKeyCode in keysDown) {
            console.log("Shortcut for discharging car at station 1.");
            var btn = $('#remove_one_ChargingStation0');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
    }

    // Station 2
    if (oneKeyCode + 1 in keysDown){
        if (cKeyCode in keysDown) {
            console.log("Shortcut for charging car at station 2.");
            var btn = $('#add_one_ChargingStation1');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
        if (dKeyCode in keysDown) {
            console.log("Shortcut for discharging car at station 2.");
            var btn = $('#remove_one_ChargingStation1');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
    }

    // Station 3
    if (oneKeyCode + 2 in keysDown){
        if (cKeyCode in keysDown) {
            console.log("Shortcut for charging car at station 3.");
            var btn = $('#add_one_ChargingStation2');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
        if (dKeyCode in keysDown) {
            console.log("Shortcut for discharging car at station 3.");
            var btn = $('#remove_one_ChargingStation2');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
       }

    // Station 4
    if (oneKeyCode + 3 in keysDown){
        if (cKeyCode in keysDown) {
            console.log("Shortcut for charging car at station 4.");
            var btn = $('#add_one_ChargingStation3');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
        if (dKeyCode in keysDown) {
            console.log("Shortcut for discharging car at station 4.");
            var btn = $('#remove_one_ChargingStation3');
            if (btn && !btn.prop('disabled')) {
                btn.click();
            }
        }
    }
}
