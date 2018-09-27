(function() {
    "use strict";

    $(document).ready(function() {
        var dt = $("#results").DataTable(window.DATATABLE_OPTIONS);
        $("form").submit(function(e) {
            var $form = $(this);
            e.preventDefault();
            $.get($form.attr("action"), $form.serialize(), function(data) {
                var results = $("#results").find("tbody").empty();
                var url = $form.attr("action") + "?" + $form.serialize();
                dt.ajax.url(url).load();
            });
        });
    });
})();
