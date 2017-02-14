$(document).ready(function () {
    $('panel-title button').click(function (e) {
        e.stopPropagation();
    });
    $('panel-title button[data-toggle="dropdown"]').click(function () {
        $('panel-title button[data-toggle="dropdown"]').dropdown('toggle')
    });
});
