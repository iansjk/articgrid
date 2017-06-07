(function () {
    "use strict";

    $(document).ready(function () {
        var dt = $("#results").DataTable(window.DATATABLE_OPTIONS);
        $("form").submit(function (e) {
            var $form = $(this);
            e.preventDefault();
            var targets = $form.find('[name^="target"]').map(function () {
                return $(this).val() || null;
            }).toArray();
            // would prefer to use $.param but that insists on escaping the '+' char
            var url = $form.attr("action") + "?" + "position=" + $("#position").val() + "&targets=" + targets.join("+");
            dt.ajax.url(url).load();
        });
    });
})();
