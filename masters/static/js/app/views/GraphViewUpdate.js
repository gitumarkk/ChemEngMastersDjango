define(["jquery", "backbone", "d3", "views/TableView", "utils/d3_graphs"],
function($, Backbone, d3, TableView, d3_graphs){
    'use strict';

    var GraphView = Backbone.View.extend({
        el: "#graph-container",
        template: "",

        initialize: function(options){
            console.log("Graph Update View Initialized");
            // _.bindAll(this, "plotSystem");
            this.graph_obj = d3_graphs.graph_container(this.el);
        },

        getDataWithD3: function(src){
            var self = this;
            d3.json(src, function(error, data){
                self.plotSystem(data);
            });
        },

        render: function() {
            return this;
        },

        plotGraph: function(){

        },
        populateGraph: function(){

        }
    });

    return GraphView;
});
