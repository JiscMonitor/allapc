jQuery(document).ready(function($) {

    /****************************************************************
     * Application Reportview Theme
     *****************************
     */

    // facetview instance for control

    function customFrame(options) {
        /*****************************************
         * overrides must provide the following classes and ids
         *
         * id: facetview - main div in which the facetview functionality goes
         * id: facetview_filters - div where the facet filters will be displayed
         * id: facetview_rightcol - the main window for result display (doesn't have to be on the right)
         * class: facetview_search_options_container - where the search bar and main controls will go
         * id : facetview_selectedfilters - where we summarise the filters which have been selected
         * class: facetview_metadata - where we want paging to go
         * id: facetview_results - the table id for where the results actually go
         * id: facetview_searching - where the loading notification can go
         *
         * Should respect the following configs
         *
         * options.debug - is this a debug enabled facetview.  If so, put a debug textarea somewhere
         */

        // the facet view object to be appended to the page
        var thefacetview = '<div id="facetview">';

        // provde the facets a place to go
        thefacetview += '<div class="row-fluid"><div class="span12"><div id="facetview_filters" style="padding-top:15px;"></div></div></div>'

        // insert loading notification
        // thefacetview += '<div class="row-fluid"><div class="span12"><div class="facetview_searching" style="display:none"></div></div></div>'

        // debug window near the bottom
        if (options.debug) {
            thefacetview += '<div class="row-fluid"><div class="span12"><div class="facetview_debug" style="display:none"><textarea style="width: 95%; height: 150px"></textarea></div></div></div>'
        }

        thefacetview += '<div style="display:none"><a href="#" class="facetview_force_search">refresh</a></div>';

        // close off the big container and return
        thefacetview += '</div>';
        return thefacetview
    }

    function customReportViewClosure(height) {
        function theReportview(options) {
            /*****************************************
             * overrides must provide the following classes and ids
             *
             * class: reportview - main div in which the reportview functionality goes, which should contain an svg element directly
             *
             * Should respect the following configs
             *
             * options.debug - is this a debug enabled reportview.  If so, put a debug textarea somewhere
             */

            // the reportview object to be appended to the page
            var thereportview = '<div class="reportview" style="height: ' + height + 'px"><svg></svg>'
            if (options.debug) {
                thereportview += "<div class='reportview_debug'><textarea style='width: 100%; height: 200px'></textarea></div>"
            }
            thereportview += '</div>';
            return thereportview
        }
        return theReportview
    }

    function updateReport(options, context) {
        var fvfilters = getFilters({"options" : options});
        var filters = [];
        if (fvfilters && fvfilters.length > 0) {
            filters = filters.concat(fvfilters)
        }

        // get the filters from the publisher autocomplete box
        var vals = $("#ac_publisher").select2("val");
        if (vals.length > 0) {
            var orfilter = {"terms" : {"monitor.dcterms:publisher.name.exact" : vals}};
            filters.push(orfilter);
        }

        $("#ac_publisher").unbind("change");
        $("#ac_publisher").change(function(event) {
            $(".facetview_force_search").trigger("click");
        });

        function statsSeries(options, facet) {
            var min_series = {"key" : "Minimum (£)", "values" : []};
            var max_series = {"key" : "Maximum (£)", "values" : []};
            // var tot_series = {"key" : "Total", "values" : []};
            var mean_series = {"key" : "Mean (£)", "values" : []};

            for (var i = 0; i < facet["values"].length; i++) {
                var result = facet["values"][i];
                var display = result[facet.facet_label_field];
                if (facet.value_function) {
                    display = facet.value_function(display)
                }
                min_series.values.push({"label": display, "value": result.min});
                max_series.values.push({"label": display, "value": result.max});
                // tot_series.values.push({"label": display, "value": result["total"]});
                mean_series.values.push({"label": display, "value": result.mean});
            }

            return [min_series, max_series, mean_series];
        }

        // hide the graphs while we re-render them
        octopus.display.hideOffScreen("#apc-count-container");
        octopus.display.hideOffScreen("#total-expenditure-container");
        octopus.display.hideOffScreen("#stats-container");

        // determine which graph we will bring back in
        var startWith = "#apc-count-container";
        if ($("#show_total").parent().hasClass("active")) {
            startWith = "#total-expenditure-container";
        } else if ($("#show_stats").parent().hasClass("active")) {
            startWith = "#stats-container";
        }

        function adjustCssClosure(selector) {

            function adjustCss(options, context) {
                // how many values do we need to display
                var num = options.data_series[0].values.length;
                var fixed_aspects = 70;
                var bar_allowance = 50;

                // calculate the new graph heights

                var report_height = bar_allowance * num + fixed_aspects;
                var container_height = report_height + 50;

                $(selector).css("height", container_height + "px")
                    .find(".reportview").css("height", report_height + "px");
            }

            return adjustCss
        }

        $('#apc-count').empty();
        $('#apc-count').report({
            type: 'horizontal_multibar',
            search_url: octopus.config.inst_query_endpoint,
            facets : [
                {
                    "type" : "terms",
                    "field" : "monitor.dcterms:publisher.name.exact",
                    "size" : 10,
                    "display" : "Number of APCs paid"
                }
            ],
            fixed_filters: filters,
            render_the_reportview: customReportViewClosure(100),
            pre_render_callback: adjustCssClosure("#apc-count")
        });

        $('#allapc-total-expenditure').empty();
        $('#allapc-total-expenditure').report({
            type: 'horizontal_multibar',
            search_url: octopus.config.inst_query_endpoint,
            facets : [
                {
                    "type" : "terms_stats",
                    "facet_value_field" : "total",
                    // "series_function": statsSeries,
                    "field" : "monitor.dcterms:publisher.name.exact",
                    "value_field" : "monitor.jm:apc.amount_gbp",
                    "size" : 10,
                    "display" : "Total Expenditure (£)"
                }
            ],
            fixed_filters: filters,
            render_the_reportview: customReportViewClosure(100),
            pre_render_callback: adjustCssClosure("#allapc-total-expenditure")
        });


        $('#allapc-stats').empty();
        $('#allapc-stats').report({
            type: 'horizontal_multibar',
            search_url: octopus.config.inst_query_endpoint,
            facets : [
                {
                    "type" : "terms_stats",
                    "series_function": statsSeries,
                    "field" : "monitor.dcterms:publisher.name.exact",
                    "value_field" : "monitor.jm:apc.amount_gbp",
                    "size" : 10,
                    "display" : "Publisher"
                }
            ],
            fixed_filters: filters,
            render_the_reportview: customReportViewClosure(100),
            pre_render_callback: adjustCssClosure("#allapc-stats")
        });

        $("#loading").hide();
        octopus.display.bringIn(startWith);
    }

    $("#facetview-controls").facetview({
        // debug: true,
        search_url: octopus.config.inst_query_endpoint,
        page_size: 0,
        facets : [
            {
                "field" : "monitor.jm:apc.name.exact",
                "display" : "Limit by Institution",
                "open" : true,
                "size" : 15
            }
        ],
        pushstate: false,
        render_the_facetview: customFrame,
        // render_facet_list: customFacetList,
        post_render_callback: updateReport
    });

    $("#show_count").click(function(event) {
        event.preventDefault();
        octopus.display.hideOffScreen("#stats-container");
        octopus.display.hideOffScreen("#total-expenditure-container");
        octopus.display.bringIn("#apc-count-container");
        $(this).parent().addClass("active");
        $("#show_stats").parent().removeClass("active");
        $("#show_total").parent().removeClass("active");
    });

    $("#show_stats").click(function(event) {
        event.preventDefault();
        octopus.display.hideOffScreen("#total-expenditure-container");
        octopus.display.hideOffScreen("#apc-count-container");
        octopus.display.bringIn("#stats-container");
        $(this).parent().addClass("active");
        $("#show_total").parent().removeClass("active");
        $("#show_count").parent().removeClass("active");
    });

    $("#show_total").click(function(event) {
        event.preventDefault();
        octopus.display.hideOffScreen("#stats-container");
        octopus.display.hideOffScreen("#apc-count-container");
        octopus.display.bringIn("#total-expenditure-container");
        $(this).parent().addClass("active");
        $("#show_stats").parent().removeClass("active");
        $("#show_count").parent().removeClass("active");
    });

    // first bind select2 to the publisher autocomplete
    octopus.esac.bindTermAutocomplete({
        selector : "#ac_publisher",
        minimumInputLength : 3,
        placeholder :"Choose publishers to display",
        type : "publisher",
        allow_clear : true,
        multiple: true
    });

    function prepDates() {
        var min = octopus.page[octopus.page.date_type];
        $("#date_from").datepicker("option", "minDate", min)
            .datepicker("option", "defaultDate", min);

        $("#date_to").datepicker("option", "minDate", min);
    }

    function loadDates(data) {
        octopus.page.date_type = "paid";
        octopus.page.applied = new Date(data.applied);
        octopus.page.paid = new Date(data.paid);
        octopus.page.published = new Date(data.published);
        prepDates();
    }

    function triggerSearch() {

        function removeRangeFacet() {
            // remove any current range facet
            var current_facets = $.fn.facetview.options.facets;
            var removes = [];
            for (var i = 0; i < current_facets.length; i++) {
                var f = current_facets[i];
                if (f.type === "range") {
                    removes.push(i);
                }
            }
            removes = removes.reverse();
            for (var i = 0; i < removes.length; i++) {
                current_facets.splice($.inArray(removes[i], current_facets), 1)
            }
        }

        // get the search ranges and field
        var fr = $("#date_from").val();
        if (fr) {
            fr = $.datepicker.parseDate("dd-mm-yy", fr);
            fr = $.datepicker.formatDate("yy-mm-dd", fr);
        }

        var to = $("#date_to").val();
        if (to) {
            to = $.datepicker.parseDate("dd-mm-yy", to);
            to = $.datepicker.formatDate("yy-mm-dd", to);
        }

        var field = "monitor.jm:apc.date_paid";
        if (octopus.page.date_type == "applied") {
            field = "jm:dateApplied";
        } else if (octopus.page.date_type == "published") {
            field = "rioxxterms:publication_date";
        }

        if (!fr && !to) {
            // remove any values and re-issue the search

            // remove any existing range facet
            removeRangeFacet();

            // unset any predefined filters
            $.fn.facetview.options.predefined_filters = {};

        } else {
            // write the new values and re-issue the search

            // create the facet that we will want to add to facetview
            var range = {};
            if (fr) {
                range["from"] = fr;
            }
            if (to) {
                range["to"] = to;
            }
            var range_facet = {
                field: field,
                type: "range",
                hidden: true,
                range : [range]
            };

            // remove the existing range facet
            removeRangeFacet();

            // add the new range facet
            $.fn.facetview.options.facets.push(range_facet);

            // create a pre-defined range filter
            var range_filter = {};
            range_filter[field] = {};
            if (fr) {
                range_filter[field]["from"] = fr;
            }
            if (to) {
                range_filter[field]["to"] = to;
            }

            // set the predefined fileter in the facetview options
            $.fn.facetview.options.predefined_filters = range_filter;
        }

        // now actually trigger a search
        $(".facetview_force_search").trigger("click");
    }

    // populate and set the bindings on the date selectors
    $("#date_from").datepicker({
        dateFormat: "dd-mm-yy",
        constrainInput: true,
        changeYear: true,
        maxDate: 0
    }).bind("change", function() {
        triggerSearch();
    });

    $("#date_to").datepicker({
        dateFormat: "dd-mm-yy",
        constrainInput: true,
        defaultDate: 0,
        changeYear: true,
        maxDate: 0
    }).bind("change", function() {
        triggerSearch();
    });

    $("#date_type").select2().bind("change", function() {
        octopus.page.date_type = $(this).select2("val");
        prepDates();

        // if dates are specified, trigger the search
        var fr = $("#date_from").val();
        var to = $("#date_to").val();
        if (to || fr) {
            triggerSearch();
        }
    });

    $.ajax({
        type: "GET",
        contentType: "application/json",
        dataType: "jsonp",
        url: "/dates",
        success: loadDates
    });

});
