
// Shortcuts

$(document).keypress(function(e) {
    console.log("Key: " + e.which);

    if (e.which == 13) {
        console.log("Enter key pressed - clicking next move.");
        $("#next_turn").click();
    }

    if (e.which == 48 + 1) {
        console.log("Shortut for charging car 1.");
    }
});
