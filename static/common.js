"use strict";

$.fn.dataTable.ext.errorMode = "throw";

$(document).ready(function () {
    $("#results").not('[data-defer-init="true"]').DataTable();
    $("form[action]").submit(function (e) {
        e.preventDefault();
        var form = $(this);
        var url = form.attr("action");
        var submit = form.find('button[type="submit"]').prop("disabled", true).text("Working...");
        $("#results").DataTable().ajax.url(url + "?" + form.serialize()).load(function() {
            submit.prop("disabled", false).text("Search");
        });
    })
});
