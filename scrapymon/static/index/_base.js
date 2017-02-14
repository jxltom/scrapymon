// Disable propagation of delete buttons in panel header so that they won't triggle toggle.
$(document).ready(function () {
    $('.panel-heading > .btn-group > button:nth-of-type(1)').click(function (e) {
        e.stopPropagation();
    });
    $('.panel-heading > .btn-group > ul button').click(function (e) {
        e.stopPropagation();
    });
    $('.panel-heading > .btn-group > button.disabled').click(function (e) {
        e.stopPropagation();
    });
});
