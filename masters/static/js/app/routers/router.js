/*global define*/
define([
    'jquery',
    'backbone',
    "views/GraphView",
    "views/LayoutView"
], function ($, Backbone, GraphView, LayoutView) {
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
                $("<div id='graph-container'></div>").appendTo("body");
            }
            var graph = new GraphView({"rate": action, src: "/reaction_rates/" + action + "/"});
            graph.render();
            self.current_view = graph;
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
                if ($("#layout").length === 0) {
                    $("<div id='layout'></div>").appendTo("body");
                }
            }

            console.log(action);
            var layout = new LayoutView({"type": "system",
                                        "system": action,
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
