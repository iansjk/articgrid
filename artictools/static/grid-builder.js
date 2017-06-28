(function () {
    "use strict";

    var TYPING_TIMEOUT = 100; // ms
    var SCROLL_PADDING = 50; // px
    var imageSearchXHR;
    var currentPage = 0;
    var maxPages;
    var imageSearchReady = true;

    $(document).ready(function () {
        var $cellContainer = $("#cell-container");
        var $gridsize = $("#grid-size");
        var $gridtitle = $("#grid-title");
        var $imageResults = $("#image-results");
        var $imageSearchQuery = $("#image-search-query");
        var $prototype = $("#prototype").children();
        var $targetImage;
        var MINIMUM_QUERY_LENGTH = parseInt($("#minimum-query-length").val());
        var S3_PICTOGRAM_URL = $("#s3-pictogram-url").val();
        var pictogramIndex = 0; // this is never reset to 0, even after new searches

        function init(savedJson) {
            $gridtitle.trigger("titleChanged");
            if (savedJson === undefined) {
                $gridsize.trigger("change");
            } else {
                $gridsize.find('option[value="' + savedJson.size + '"]').prop("selected", true);
                if (savedJson.title) {
                    $gridtitle.text(savedJson.title).trigger("titleChanged");
                }
                var $row = $('<div class="row">').appendTo($cellContainer);
                for (var i = 0; i < savedJson.cells.length; i++) {
                    if (i % savedJson.size === 0) {
                        $row = $row.clone().empty().appendTo($cellContainer);
                    }
                    var celldata = savedJson.cells[i];
                    var $cell = $prototype.clone();
                    if (celldata.id) {
                        $cell.find(".cell-image")
                            .attr("src", S3_PICTOGRAM_URL + "/" + celldata.id + ".png")
                            .attr("data-pictogram-id", celldata.id);
                    }
                    if (celldata.label) {
                        $cell.find(".cell-title").text(celldata.label);
                    }
                    $row.append($cell);
                }
                $cellContainer.find(".cell").trigger("cellChanged");
                updateUrl();
            }
        }

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
                if ($cell.hasClass("hidden-print")) {
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

        function renderPictogramResponse(json) {
            for (var i = 0; i < json.data.length; i++, pictogramIndex++) {
                var celldata = json.data[i];
                for (var j = 0; j < celldata[1].length; j++, pictogramIndex++) {
                    var $col = $('<div class="col-3">').appendTo($imageResults);
                    $('<input type="radio" name="pictogram" id="pictogram' + pictogramIndex + '">').appendTo($col);
                    $('<label for="pictogram' + pictogramIndex + '">').append($('<img class="img-fluid">')
                        .attr("alt", celldata[0])
                        .attr("data-pictogram-id", celldata[1][j])
                        .attr("data-original", S3_PICTOGRAM_URL + "/" + celldata[1][j] + ".png")
                        .attr("width", 80)
                        .attr("height", 80).appendTo($col).tooltip({
                            "animation": false,
                            "title": function () {
                                return this.alt;
                            }
                        })
                    ).appendTo($col);
                }
            }
            $imageResults.find("img").lazyload({
                "container": $imageResults
            });
        }

        function search() {
            var $form = $imageSearchQuery.parents("form");
            var params = {
                "query": $("#image-search-query").val().trim(),
                "page": 0
            };
            imageSearchXHR = $.get($form.attr("action") + "?" + $.param(params), function (json) {
                $imageResults.siblings(".placeholder").hide();
                if (json.data.length === 0) {
                    $imageResults.html('<span class="no-results">No image results found.</span>');
                } else {
                    $imageResults.empty();
                    renderPictogramResponse(json);
                    currentPage = 1;
                    maxPages = json.maxPages;

                    var $modalBody = $imageResults.parent().on("scroll", function () {
                        if (imageSearchReady === false) {
                            return false;
                        }

                        var elem = this;
                        if (elem.scrollHeight - elem.scrollTop <= elem.clientHeight + SCROLL_PADDING) {
                            if (currentPage > maxPages) {
                                $(elem).off("scroll");
                            } else {
                                params.page++;
                                $imageResults.siblings(".placeholder").show();
                                $.get($form.attr("action") + "?" + $.param(params), function (json) {
                                    renderPictogramResponse(json);
                                }).done(function () {
                                    $imageResults.siblings(".placeholder").hide();
                                });
                                currentPage++;
                            }
                        }
                        imageSearchReady = true;
                    });

                    // immediately load more if not scrollable + still more to fetch
                    if ($modalBody[0].scrollHeight <= $modalBody[0].clientHeight && currentPage <= maxPages) {
                        $modalBody.trigger("scroll");
                    }
                }
            });
        }

        $("#grid").on("cellChanged", ".cell", function (_, params) {
            var $cell = $(this);
            var $cellTitle = $cell.find(".cell-title");
            var $cellImage = $cell.find(".cell-image");
            $cellTitle.toggleClass("hidden-print text-muted", $cellTitle.text().trim() === $cellTitle.attr("data-placeholder"));
            $cellImage.toggleClass("hidden-print", $cellImage.attr("src") === undefined || $cellImage.attr("src").startsWith("data:"));
            $cell.toggleClass("hidden-print", $cellTitle.hasClass("hidden-print") && $cellImage.hasClass("hidden-print"));
            if (!params || params.deferUpdateUrl !== true) {
                updateUrl();
            }
        }).on("titleChanged", "#grid-title", function () {
            var $this = $(this);
            $this.toggleClass("text-muted hidden-print", $this.text().trim() === $this.attr("data-placeholder"));
            updateUrl();
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
            if ($this.attr("id") === "grid-title") {
                $this.trigger("titleChanged");
            } else if ($this.hasClass("cell-title")) {
                $this.closest(".cell").trigger("cellChanged");
            }
        }).on("keypress", "#grid-title, .cell-title", function (e) {
            // disallow newline (enter key)
            return e.which !== 13;
        });

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

        $("#print").click(function (e) {
            e.preventDefault();
            window.print();
        });

        var typingTimer;
        $imageSearchQuery.on("input propertychange paste", function () {
            if (imageSearchXHR) {
                imageSearchXHR.abort();
            }
            clearTimeout(typingTimer);
            if ($imageSearchQuery.val().length >= MINIMUM_QUERY_LENGTH) {
                typingTimer = setTimeout(search, TYPING_TIMEOUT);
                $imageResults.empty().siblings(".placeholder").show();
            }
        });

        var $imagePicker = $("#image-picker");
        $imagePicker.on("show.bs.modal", function (e) {
            $targetImage = $(e.relatedTarget);
            var $cellTitle = $targetImage.siblings(".cell-title");
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
            var $selectedRadio = $imageResults.find('input[name="pictogram"]:checked');
            var $selectedImage = $selectedRadio.siblings("label").children("img");
            if ($selectedImage) {
                $targetImage.attr("src", $selectedImage.attr("src"))
                    .attr("data-pictogram-id", $selectedImage.attr("data-pictogram-id"));
                $targetImage.closest(".cell").trigger("cellChanged");
            }
            $imagePicker.modal("hide");
        });

        $("#reset-image").click(function (e) {
            e.preventDefault();
            $targetImage.removeAttr("src");
            Holder.run({images: $targetImage[0]});
            $targetImage.closest(".cell").trigger("cellChanged");
            $imagePicker.modal("hide");
        });

        // initialize or load from saved url
        var savedGrid;
        try {
            savedGrid = JSON.parse(window.location.hash.slice(1));
        } catch (e) {
            // noop
        }
        init(savedGrid);
    });
}());
