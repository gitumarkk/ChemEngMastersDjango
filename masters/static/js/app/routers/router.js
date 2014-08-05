/*global define*/
define([
    'jquery',
    'backbone',
    "views/GraphView",
    "views/LayoutView",
    "views/RatesView"
], function ($, Backbone, GraphView, LayoutView, RatesView) {
    'use strict';

    var AppRouter = Backbone.Router.extend({
        initialize: function(options) {
            self.current_view = undefined;
            console.log("initialized");
        },

        routes: {
            'reactions/:action': "reactionRates",
            'reactors/:action': "reactors",
            'system/:action': "system",
            // 'reset': "reset",
        },

        reactionRates : function(action){
            if (self.current_view) {
                self.current_view.close();
            }
            // var graph = new GraphView({"rate": action, src: "/reaction_rates/" + action + "/"});
            // graph.render();
            // self.current_view = graph;

            var rates_layout = new LayoutView({"type": "rates",
                                                "action": action,
                                                src: "/system_run/" + action + "/"});

            // var rates = new RatesView({"rate": action, src: "/reaction_rates/" + action + "/"});
            // rates.render();
            self.current_view = rates_layout;
        },
        reactors: function(action){
            if (self.current_view) {
                self.current_view.close();
                $("<div id='graph-container'></div>").appendTo("body");
            }
            var graph = new GraphView({"reactor": action, src: "/single_reactor/" + action + "/"});
            graph.render();
            self.current_view = graph;
        },
        system: function(action){
            if (self.current_view) {
                self.current_view.close();
            }

            console.log(action);
            var layout = new LayoutView({"type": "system",
                                        "action": action,
                                        src: "/system_run/" + action + "/"});
            self.current_view = layout;
        },
        reset: function(){
            console.log("Reset");
            var el = self.current_view.el;
            if (self.current_view) {self.current_view.close();}
        }
    });

    return AppRouter;
});
