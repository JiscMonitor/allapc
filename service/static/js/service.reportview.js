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
        thefacetview += '<div class="row-fluid"><div class="span12"><div id="facetview_filters" style="padding-top:45px;"></div></div></div>'

        // insert loading notification
        // thefacetview += '<div class="row-fluid"><div class="span12"><div class="facetview_searching" style="display:none"></div></div></div>'

        // debug window near the bottom
        if (options.debug) {
            thefacetview += '<div class="row-fluid"><div class="span12"><div class="facetview_debug" style="display:none"><textarea style="width: 95%; height: 150px"></textarea></div></div></div>'
        }

        // close off the big container and return
        thefacetview += '</div>';
        return thefacetview
    }

    function customFacetList(options) {
        /*****************************************
         * overrides must provide the following classes and ids
         *
         * none - no requirements for specific classes and ids
         *
         * should (not must) respect the following config
         *
         * options.facet[x].hidden - whether the facet should be displayed in the UI or not
         * options.render_terms_facet - renders a term facet into the list
         * options.render_range_facet - renders a range facet into the list
         * options.render_geo_facet - renders a geo distance facet into the list
         */
        if (options.facets.length > 0) {
            var filters = options.facets;
            var thefilters = '';

            // insert our own select2 filter
            thefilters += "<input type='text' name='publisher' id='ac_publisher' style='width: 100%; margin-bottom: 40px;'>";

            for (var idx = 0; idx < filters.length; idx++) {
                var facet = filters[idx]
                // if the facet is hidden do not include it in this list
                if (facet.hidden) {
                    continue;
                }

                var type = facet.type ? facet.type : "terms"
                if (type === "terms") {
                    thefilters += options.render_terms_facet(facet, options)
                } else if (type === "range") {
                    thefilters += options.render_range_facet(facet, options)
                } else if (type === "geo_distance") {
                    thefilters += options.render_geo_facet(facet, options)
                }
                // FIXME: statistical facet and terms_stats facet?
            };
            return thefilters
        };
        return ""
    };


    var hideDetails = {};
    function hideOffScreen(selector) {
        var el = $(selector);
        if (selector in hideDetails) { return }
        hideDetails[selector] = {"position" : el.css("position"), "margin" : el.css("margin-left")};
        $(selector).css("position", "absolute").css("margin-left", -9999);
    }
    function bringIn(selector) {
        var pos = hideDetails[selector].position;
        var mar = hideDetails[selector].margin
        $(selector).css("position", pos).css("margin-left", mar);
        delete hideDetails[selector];
    }

    function updateReport(options, context) {
        var fvfilters = getFilters({"options" : options});

        // first bind select2 to the publisher autocomplete
        octopus.esac.bindTermAutocomplete({
            selector : "#ac_publisher",
            minimumInputLength : 3,
            placeholder :"Choose publishers to display",
            type : "publisher",
            allow_clear : true,
            multiple: true
        });

        $("#ac_publisher").change(function(event) {
            alert("oi");
        })

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
        hideOffScreen("#total-expenditure-container");
        hideOffScreen("#stats-container");

        // determine which graph we will bring back in
        var startWith = "#total-expenditure-container";
        if ($("#show_stats").parent().hasClass("active")) {
            startWith = "#stats-container";
        }

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
            fixed_filters: fvfilters
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
            fixed_filters: fvfilters
        });

        $("#loading").hide();
        bringIn(startWith);
    }

    $("#facetview-controls").facetview({
        // debug: true,
        search_url: octopus.config.inst_query_endpoint,
        page_size: 0,
        facets : [
            //{
            //    "field" : "monitor.dcterms:publisher.name.exact",
            //    "display" : "Publisher",
            //    "open" : true,
            //    "size" : 10
            //},
            {
                "field" : "monitor.jm:apc.name.exact",
                "display" : "Limit by Institution",
                "open" : true,
                "size" : 50
            }
        ],
        pushstate: false,
        render_the_facetview: customFrame,
        render_facet_list: customFacetList,
        post_render_callback: updateReport
    });

    $("#show_stats").click(function(event) {
        event.preventDefault();
        hideOffScreen("#total-expenditure-container");
        bringIn("#stats-container");
        $(this).parent().addClass("active");
        $("#show_total").parent().removeClass("active");
    });

    $("#show_total").click(function(event) {
        event.preventDefault();
        hideOffScreen("#stats-container");
        bringIn("#total-expenditure-container");
        $(this).parent().addClass("active");
        $("#show_stats").parent().removeClass("active");
    });
});
