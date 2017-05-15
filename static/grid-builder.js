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

        var $imageResults = $("#image-results");
        var $imageSearchQuery = $("#image-search-query");
        var typingTimer;
        var doneTypingInterval = 2000;

        $imageSearchQuery.on("input propertychange paste", function () {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(doneTyping, doneTypingInterval);
            $imageResults.empty().siblings(".placeholder").show();
        });

        function doneTyping() {
            var $form = $imageSearchQuery.parents("form");
            var url = $form.attr("action");
            $.get(url + "?" + $form.serialize(), function (json) {
                $imageResults.siblings(".placeholder").hide();
                if (json.data.length === 0) {
                    $imageResults.html('<span class="no-results">No image results found.</span>');
                } else {
                    for (var i = 0; i < json.data.length; i++) {
                        var celldata = json.data[i];
                        for (var j = 0; j < celldata[1].length; j++) {
                            var $col = $('<div class="col-3">').appendTo($imageResults);
                            $('<img class="img-fluid">').attr("alt", celldata[0]).attr("src", celldata[1][j]).appendTo($col).tooltip({
                                "animation": false,
                                "title": function() {
                                    return this.alt;
                                }
                            });
                        }
                    }
                }
                $imageResults.find("img").imgCheckbox({
                    "radio": true,
                    "graySelected": false,
                    "onclick": function(e) {
                        console.log(e);
                    }
                });
            });
        }

        var $imagePicker = $("#image-picker");
        $imagePicker.on("show.bs.modal", function (e) {
            var $target = $(e.relatedTarget).attr("id", "target");
            var $cellTitle = $target.siblings(".cell-title");
            var cellTitleText = $cellTitle.text().trim();
            var $imageSearchQuery = $imagePicker.find("#image-search-query");
            if (cellTitleText !== "" && cellTitleText !== $cellTitle.attr("data-placeholder")) {
                $imageSearchQuery.val(cellTitleText).trigger("input");
            } else {
                $imageSearchQuery.val("");
            }
        });

        $("#save").click(function(e) {
            e.preventDefault();
            var $target = $("#target");
            var selectedImgUrl = $imageResults.find(".imgChked").children("img").attr("src");
            if (selectedImgUrl) {
                $target.attr("src", selectedImgUrl);
            }
            $target.removeAttr("id");
            $imagePicker.modal("hide");
        });
    });
}());
