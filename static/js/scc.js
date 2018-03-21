$(document).ready(function() {

    data = 'hey';
    $('.alert').alert();
    $("#dialog").dialog({ show: 'fade', hide: 'drop' });
    addAlert(data, true, null);
});

function addAlert(data, autoClose, id) {
    console.log('test')
    var type = data.status == 'ERROR' ? 'danger' : data.status == 'OK' ? 'success' : 'info';
    var icon = data.status == 'ERROR' ? 'times-circle' : data.status == 'OK' ? 'check-circle' : 'refresh fa-spin';
    var alert = $('<div class="alert alert-' + type + ' alert-dismissible fade in" role="alert">')
            .append(
                    $('<button type="button" class="close" data-dismiss="alert">')
                    .append('&times;')
                    )
            .append($('<span class="fa fa-' + icon + '" aria-hidden="true"></span> ' +
                    '<span class="sr-only">' + data.status + ': </span>'))
            .append(data.message);
    if (id != null)
        alert.attr('id', id);
    $('#alerts').append(alert);
    if (autoClose)
        alert.delay(5000).fadeOut('slow', function () {
            $(this).alert('close');
        });
}
