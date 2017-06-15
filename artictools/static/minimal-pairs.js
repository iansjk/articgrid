(function() {
    "use strict";

    $(document).ready(function() {
        var dt = $("#results").DataTable(window.DATATABLE_OPTIONS);
        var $form = $("form");
        $form.submit(function(e) {
            e.preventDefault();
            dt.ajax.url($form.attr("action") + "?" + $form.serialize()).load();
        });
    });
})();
