/*global define*/
define([
    'jquery',
    'backbone',
    "views/GraphView"
], function ($, Backbone, GraphView) {
    'use strict';

    var AppRouter = Backbone.Router.extend({
        initialize: function(options) {
        },

        routes: {
            // '*filter': 'defaultRoute',
            // 'reactionRates/:copper': "reactionRates",
            'reactions/:action': "reactionRates",
        },

        reactionRates : function(action){
            var graph = new GraphView({"rate": action, src: "/reaction_rates/" + action + "/"});
            graph.render();
        }
    });

    return AppRouter;
});
