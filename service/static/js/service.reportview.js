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

    function updateReport(options, context) {
        var fvfilters = getFilters({"options" : options});

        function statsSeries(options, facet) {
            var min_series = {"key" : "Minimum", "values" : []};
            var max_series = {"key" : "Maximum", "values" : []};
            var tot_series = {"key" : "Total", "values" : []};
            var mean_series = {"key" : "Mean", "values" : []};

            for (var i = 0; i < facet["values"].length; i++) {
                var result = facet["values"][i];
                var display = result[facet.facet_label_field];
                if (facet.value_function) {
                    display = facet.value_function(display)
                }
                min_series.values.push({"label": display, "value": result.min});
                max_series.values.push({"label": display, "value": result.max});
                tot_series.values.push({"label": display, "value": result["total"]});
                mean_series.values.push({"label": display, "value": result.mean});
            }

            return [tot_series, min_series, max_series, mean_series];
        }

        $('#allapc_total_expenditure').empty();
        $('#allapc_total_expenditure').report({
            type: 'horizontal_multibar',
            search_url: octopus.config.inst_query_endpoint,
            facets : [
                {
                    "type" : "terms_stats",
                    // "facet_value_field" : "total",
                    "series_function": statsSeries,
                    "field" : "monitor.dcterms:publisher.name.exact",
                    "value_field" : "monitor.jm:apc.amount_gbp",
                    "size" : 10,
                    "display" : "Publisher"
                }
            ],
            fixed_filters: fvfilters //,
            //pre_render_callback: reduceAspectDataSeries
        });

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
        post_render_callback: updateReport
    })
});
