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

    // disallow newline (enter key) in grid title
    $("#grid-title").keypress(function (e) {
        return e.which !== 13;
    });

    $("#grid").on("focusin", "h2, h4", function () {
        var $this = $(this);
        if ($this.text().trim() === $this.attr("data-placeholder")) {
            $this.removeClass("text-muted").text("");
        }
    }).on("focusout", "h2, h4", function () {
        var $this = $(this);
        if ($this.text().trim() === "") {
            $this.addClass("text-muted").text($this.attr("data-placeholder"));
        }
    });
});
