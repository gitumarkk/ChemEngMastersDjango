/*
* The Layout is use dto manage the views in a single url route
* It gets the route action, gets the data and renders the different
* graph views depending on the data returned
* At the moment it is used in the reactor system and not individual graphs
*/
define(["jquery",
"backbone",
"d3",
"views/GraphViewUpdate",
"views/SummaryView"],
function($, Backbone, d3, GraphView, SummaryView){
    var LayoutView = Backbone.View.extend({
        el: "#layout",
        initialize: function(options){
            var self = this;

            _.bindAll(self, "assignViews");
            self.views_list = [];  // Holds an array of the current views
            console.log("layout initialized");

            self.type = options.type;
            self.system = options.system;
            self.src = options.src;

            self.fetchDataWithD3();
        },

        fetchDataWithD3: function(){
            var self = this;
            d3.json(self.src, function(error, data){
                self.assignViews(data);
            });
        },

        /*
        This view generates the required views based on the data coming form the back end
        */
        assignViews: function(data){
            var summary = new SummaryView({data: data.summary});
            // var bioxidation = new GraphView({});
            // var chemical = new GraphView();
        },

        renderGraphViews: function(data){
            var ferric_view, summary_view, setup_view, cost_view;
            ferric_view = new GraphView();
        }
    });
    return LayoutView;
});
