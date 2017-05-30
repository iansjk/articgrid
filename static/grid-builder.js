(function () {
    "use strict";

    $(document).ready(function () {
        var $gridsize = $("#grid-size");
        var $cellContainer = $("#cell-container");
        var $gridtitle = $("#grid-title");
        function updateUrl() {
            var title = $gridtitle.text().trim();
            var currentState = {
                "title": title === $gridtitle.attr("data-placeholder") ? "" : title,
                "size": parseInt($gridsize.val()),
                "cells": []
            };
            var $cells = $cellContainer.find(".cell");
            for (var i = 0; i < $cells.length; i++) {
                var $cell = $($cells[i]);
                if ($cell.hasClass("empty")) {
                    currentState.cells.push({});
                } else {
                    var $cellTitle = $cell.find(".cell-title");
                    var label = $cellTitle.text().trim();
                    currentState.cells.push({
                        "id": parseInt($cell.find(".cell-image").attr("data-pictogram-id")) || 0,
                        "label": label === $cellTitle.attr("data-placeholder") ? "" : label
                    });
                }
            }
            window.location.hash = JSON.stringify(currentState);
        }

        $("#grid").on("cellChanged", ".cell", function (_, params) {
            var $cell = $(this);
            var $cellTitle = $cell.find(".cell-title");
            var $cellImage = $cell.find(".cell-image");
            $cellTitle.toggleClass("empty text-muted", $cellTitle.text().trim() === $cellTitle.attr("data-placeholder"));
            $cellImage.toggleClass("empty", $cellImage.attr("src") === undefined || $cellImage.attr("src").startsWith("data:"));
            $cell.toggleClass("empty", $cellTitle.hasClass("empty") && $cellImage.hasClass("empty"));
            if (!params || params.deferUpdateUrl !== true) {
                updateUrl();
            }
        }).on("focusin", "#grid-title, .cell-title", function () {
            var $this = $(this);
            if ($this.text().trim() === $this.attr("data-placeholder")) {
                $this.removeClass("text-muted").text("");
            }
        }).on("focusout", "#grid-title, .cell-title", function () {
            var $this = $(this);
            if ($this.text().trim() === "") {
                $this.addClass("text-muted").text($this.attr("data-placeholder"));
            }
            $this.closest(".cell").trigger("cellChanged");
        }).on("keypress", "#grid-title, .cell-title", function (e) {
            // disallow newline (enter key)
            return e.which !== 13;
        });

        var $prototype = $("#prototype").children();
        $gridsize.change(function () {
            $cellContainer.empty();
            for (var i = 0; i < $gridsize.val(); i++) {
                var $row = $('<div class="row">');
                for (var j = 0; j < $gridsize.val(); j++) {
                    var $cell = $prototype.clone();
                    $cell.appendTo($row);
                }
                $row.appendTo($cellContainer);
            }
            $cellContainer.find(".cell").trigger("cellChanged", {"deferUpdateUrl": true});
            updateUrl();
        });

        var savedGrid;
        try {
            savedGrid = JSON.parse(window.location.hash.slice(1));
        } catch (e) {
            // noop
        }
        if (savedGrid === undefined) {
            $gridsize.trigger("change"); // initialize the grid
        } else {
            var $row = $('<div class="row">').appendTo($cellContainer);
            for (var i = 0; i < savedGrid.cells.length; i++) {
                if (i % savedGrid.size === 0) {
                    $row = $row.clone().empty().appendTo($cellContainer);
                }
                var celldata = savedGrid.cells[i];
                var $cell = $prototype.clone();
                if (celldata.id) {
                    $cell.find(".cell-image")
                        .attr("src", Flask.url_for("static_pictogram", {"pictogram_id": celldata.id}))
                        .attr("data-pictogram-id", celldata.id);
                }
                if (celldata.label) {
                    $cell.find(".cell-title").text(celldata.label);
                }
                $row.append($cell.trigger("cellChanged", {"deferUpdateUrl": true}));
            }
        }

        $("#print").click(function (e) {
            e.preventDefault();
            window.print();
        });

        var $imageResults = $("#image-results");
        var $imageSearchQuery = $("#image-search-query");
        var typingTimer;
        var doneTypingInterval = 500; // ms

        $imageSearchQuery.on("input propertychange paste", function () {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(search, doneTypingInterval);
            $imageResults.empty().siblings(".placeholder").show();
        });

        function search() {
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
                            $('<img class="img-fluid">')
                                .attr("alt", celldata[0])
                                .attr("data-pictogram-id", celldata[1][j])
                                .attr("src", Flask.url_for("static_pictogram", {"pictogram_id": celldata[1][j]}))
                                .attr("width", 80)
                                .attr("height", 80).appendTo($col).tooltip(
                                {
                                    "animation": false,
                                    "title": function () {
                                        return this.alt;
                                    }
                                });
                        }
                    }
                }
                $imageResults.find("img").imgCheckbox({
                    "radio": true,
                    "graySelected": false
                });
            });
        }

        var $imagePicker = $("#image-picker");
        $imagePicker.on("show.bs.modal", function (e) {
            var $target = $(e.relatedTarget).attr("id", "target-image");
            var $cellTitle = $target.siblings(".cell-title");
            var cellTitleText = $cellTitle.text().trim();
            var $imageSearchQuery = $imagePicker.find("#image-search-query");
            if (cellTitleText !== "" && cellTitleText !== $cellTitle.attr("data-placeholder")) {
                $imageSearchQuery.val(cellTitleText);
                $imageResults.empty().siblings(".placeholder").show();
                search();
            } else {
                $imageSearchQuery.val("");
            }
        });

        $("#save").click(function (e) {
            e.preventDefault();
            var $targetImage = $("#target-image");
            var selectedImage = $imageResults.find(".imgChked").children("img");
            if (selectedImage) {
                $targetImage.attr("src", selectedImage.attr("src"))
                    .attr("data-pictogram-id", selectedImage.attr("data-pictogram-id"));
            }
            $targetImage.removeAttr("id").closest(".cell").trigger("cellChanged");
            $imagePicker.modal("hide");
        });

        $("#reset-image").click(function (e) {
            e.preventDefault();
            var $targetImage = $("#target-image").removeAttr("src");
            Holder.run({images: document.getElementById("target-image")});
            $targetImage.removeAttr("id").closest(".cell").trigger("cellChanged");
            $imagePicker.modal("hide");
        });
    });
}());
