jQuery(document).ready(function($) {

    /****************************************************************
     * ALL APC Facetview Theme
     *****************************
     */

    function discoveryRecordView(options, record) {
        var result = options.resultwrap_start;
        var monitor = record["monitor"];

        var issn = "";
        if (monitor.hasOwnProperty("dc:source") && monitor["dc:source"].hasOwnProperty("identifier")) {
            var sis = monitor["dc:source"]["identifier"];
            if (sis.length > 0) {
                if (sis[0].hasOwnProperty("id")) {
                    issn = " (ISSN:" + monitor["dc:source"]["identifier"][0]["id"] + ")";
                }
            }
        }

        var fund = "";
        if (monitor["jm:apc"][0]["fund"]) {
            for (var i = 0; i < monitor["jm:apc"][0]["fund"].length; i++) {
                var f = monitor["jm:apc"][0]["fund"][i];
                if (fund !== "") {
                    fund += ", "
                }
                fund += f["name"]
            }
            fund = " / " + fund
        }

        var publisher_name = monitor["dcterms:publisher"] ? monitor["dcterms:publisher"]["name"] : "";
        var source_name = monitor["dc:source"] ? monitor["dc:source"]["name"] : "";
        var funder_name = monitor["rioxxterms:project"] && monitor["rioxxterms:project"].length > 0 ? monitor["rioxxterms:project"][0]["name"] : "";

        result += "<div class='row-fluid' style='margin-top: 10px; margin-bottom: 10px'>";
        result += "<div class='span10'>";
        var title = monitor["dc:title"] ? monitor["dc:title"] : "Untitled";
        result += "<strong style='font-size: 150%'>" + title + "</strong><br>";
        result += publisher_name + " - " + source_name + issn + "<br>";
        result += funder_name + " - " + monitor["jm:apc"][0]["name"] + fund;

        var cost = monitor["jm:apc"][0]["amount_gbp"];
        if (!cost) { cost = " unknown"}
        result += "</div><div class='span2'>";
        result += "<strong style='font-size: 150%'>£" + cost + "</strong><br>";
        if (monitor["jm:apc"][0]["additional_costs"]) {
            result += "£" + monitor["jm:apc"][0]["additional_costs"] + " additional costs<br>";
        }
        if (monitor["license_ref"]) {
            result += monitor["license_ref"]["title"];
        }
        result += "</div></div>";
        result += options.resultwrap_end;
        return result;
    }

    var facets = [];
    facets.push({'field': 'monitor.dc:source.name.exact', 'display': 'Journal'});
    facets.push({'field': 'monitor.dc:source.identifier.id.exact', 'display': 'ISSN'});
    facets.push({'field': 'monitor.dcterms:publisher.name.exact', 'display': 'Publisher'});
    facets.push({'field': 'monitor.rioxxterms:project.name.exact', 'display': 'Funder'});
    facets.push({'field': 'monitor.jm:apc.name.exact', 'display': 'Organisation'});
    facets.push({'field': 'monitor.jm:apc.fund.name.exact', 'display': 'Paid from fund'});
    facets.push({'field': 'monitor.license_ref.title.exact', 'display': 'Licence Requested'});

    // FIXME: can't have a range search until the underlying data is numeric
    //facets.push({
    //    "field" : "monitor.jm:apc.amount_gbp",
    //    "display" : "APC Cost",
    //    "type" : "range",
    //    "range" : [
    //        { "from" : 0, "to" : 100, "display" : "£0 - £100" }
    //    ]
    //})
    // range on monitor.jm:apc.amount_gbp

    $('#allapc_facetview').facetview({
        debug: false,
        search_url : octopus.config.inst_query_endpoint,
        page_size : 25,
        facets : facets,
        search_sortby : [
            //{'display':'Date Applied','field':'monitor.jm:dateApplied'},
            //{'display':'Title','field':'monitor.dc:title'},
            //{'display':'Publication Date','field':'monitor.rioxxterms:publication_date'},
            //{'display':'APC Cost','field':'monitor.jm:apc.amount_gbp'}
        ],
        searchbox_fieldselect : [],
        render_result_record : discoveryRecordView

    });

});
