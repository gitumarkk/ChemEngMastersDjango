/*global define*/
define([
    'jquery',
    'backbone',
    "views/GraphViewUpdate",
    "views/LayoutView"
], function ($, Backbone, GraphView, LayoutView) {
    'use strict';

    var AppRouter = Backbone.Router.extend({
        initialize: function(options) {
        },

        routes: {
            // '*filter': 'defaultRoute',
            // 'reactionRates/:copper': "reactionRates",
            'reactions/:action': "reactionRates",
            'reactors/:action': "reactors",
            // 'system/:action': "system",
            'system/:action': "system",
        },

        reactionRates : function(action){
            var graph = new GraphView({"rate": action, src: "/reaction_rates/" + action + "/"});
            graph.render();
        },
        reactors: function(action){
            var graph = new GraphView({"reactor": action, src: "/single_reactor/" + action + "/"});
            graph.render();
        },
        // system: function(action){
        //     console.log("system");
        //     console.log(action);
        //     var graph = new GraphView({"system": action, src: "/system_run/" + action + "/"});
        //     graph.render();
        // },
        system: function(action){
            // console.log("system");
            // console.log(action);
            // var graph = new GraphView({"system": action, src: "/system_run/" + action + "/"});
            // graph.render();
            var layout = new LayoutView({"type": "system",
                                        "system": action,
                                        src: "/system_run/" + action + "/"});
        },
        test_layout: function(action){
            console.log("test initialized");
            // var LayoutView = require("views/LayoutView");
            var layout_sytem = new LayoutView();
        }
    });

    return AppRouter;
});
