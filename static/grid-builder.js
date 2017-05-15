(function () {
    "use strict";

    $(document).ready(function () {
        var $prototype = $("#prototype").children();
        var $gridsize = $("#grid-size");
        var $gridcells = $("#grid-cells");
        $gridsize.change(function () {
            $gridcells.empty();
            for (var i = 0; i < $gridsize.val(); i++) {
                var $row = $('<div class="row">');
                for (var j = 0; j < $gridsize.val(); j++) {
                    $prototype.clone().appendTo($row);
                }
                $row.appendTo($gridcells);
            }
        }).trigger("change");

        $("#print").click(function (e) {
            e.preventDefault();
            window.print();
        });

        // disallow newline (enter key)
        $("#grid-title, .cell-title").keypress(function (e) {
            return e.which !== 13;
        });

        $("#grid").on("focusin", "#grid-title, .cell-title", function () {
            var $this = $(this);
            if ($this.text().trim() === $this.attr("data-placeholder")) {
                $this.removeClass("text-muted").text("");
            }
        }).on("focusout", "#grid-title, .cell-title", function () {
            var $this = $(this);
            if ($this.text().trim() === "") {
                $this.addClass("text-muted").text($this.attr("data-placeholder"));
            }
        });

        var $imagePicker = $("#image-picker");
        $imagePicker.on("show.bs.modal", function (e) {
            var $cellTitle = $(e.relatedTarget).siblings(".cell-title");
            var cellTitleText = $cellTitle.text().trim();
            var $imageSearchQuery = $imagePicker.find("#image-search-query");
            if (cellTitleText !== "" && cellTitleText !== $cellTitle.attr("data-placeholder")) {
                $imageSearchQuery.val(cellTitleText);
            } else {
                $imageSearchQuery.val("");
            }
        });
    });
}());
