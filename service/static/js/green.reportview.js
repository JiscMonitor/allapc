jQuery(document).ready(function($) {

    /****************************************************************
     * Application Reportview Theme
     *****************************
     */

    function lookupStats(options) {
        var sum_of_facets = 0;
        for (var i = 0; i < options.facets.length; i++) {
            var facet = options.facets[i];
            if (facet.field === "index.green_option.exact") {
                for (var j = 0; j < facet.values.length; j++) {
                    var result = facet.values[j];
                    sum_of_facets += result.count;
                }
            }
        }
        return {"total" : options.data.found, "sum" : sum_of_facets, "undetected" : options.data.found - sum_of_facets}
    }

    function populateBlurb(options, context) {
        /*
        From a total of <span id="total">[total]</span> APC Records,
        <span id="detected">[detected]</span> could be looked up in
        <a href="http://www.sherpa.ac.uk/fact/index.php">Sherpa Fact</a>, and
        <span id="undetected">[undetected]</span> could not.
        */
        var stats = lookupStats(options);

        $("#total").html(stats.total);
        $("#detected").html(stats.sum);
        $("#undetected").html(stats.undetected);

        $("#blurb_container").show()
    }

    function prefixTotal(options, facet) {
        var stats = lookupStats(options);

        var series = {};
        series["key"] = "Numbers of APCs";
        series["values"] = [];
        series.values.push({"label" : "Total APCs", "value" : stats.total});
        for (var i = 0; i < facet["values"].length; i++) {
            var result = facet["values"][i];
            var display = result[facet.facet_label_field];
            if (facet.value_function) {
                display = facet.value_function(display)
            }
            series.values.push({"label": display, "value": result[facet.facet_value_field]})
        }

        series.values.push({"label" : "Unable to look up", "value" : stats.undetected});
        return series;
    }

    function complianceMap(value) {
        var vmap = {
            "no" : "No Green",
            "yes" : "Green Available",
            "maybe" : "Maybe Green Available",
            "unknown" : "Could not tell"
        };
        return vmap[value]
    }

    $('#gold-green').empty();
    $('#gold-green').report({
        type: 'multibar',
        search_url: octopus.config.inst_query_endpoint,
        facets : [
            {
                "type" : "terms",
                "field" : "index.green_option.exact",
                "size" : 10,
                "display" : "Green Option",
                "series_function" : prefixTotal,
                "value_function" : complianceMap
            }
        ],
        post_render_callback: populateBlurb
    });
});
