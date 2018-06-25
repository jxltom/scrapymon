$(document).ready(function () {
    // Disable propagation of delete buttons in card header so that they won't triggle toggle.
    $('.card-header > .btn-group > button:nth-of-type(1)').click(function (e) {
        e.stopPropagation();
        //$('.card-header > .btn-group > ul button').dropdown('toggle');
    });
    $('.card-header > .btn-group > ul button').click(function (e) {
        e.stopPropagation();
        //$('.card-header > .btn-group > ul button').dropdown('toggle');
    });

    // Schedule spider run.
    $('[role="schedule"]').click(function () {
        $.get(this.id, function () {
            window.location = location.href;
        });
    });
    // Cancel job.
    $('[role="cancel"]').click(function () {
        $.get(this.id, function () {
            window.location = location.href;
        });
    });
    // Delete project or a specific version.
    $('[role="delete"]').click(function () {
        $.get(this.id, function () {
            window.location = location.href;
        });
    });
    // Get job jog .
    $('[role="logs"]').click(function () {
        window.location = this.id;
    });
});
