/*global require*/
'use strict';

require.config({
    // baseUrl: "/",
    waitSeconds: 0,
    shim: {
        underscore: {
            exports: '_'
        },
        backbone: {
            deps: [
                'underscore',
                'jquery'
            ],
            exports: 'Backbone'
        },
        foundation: {
            deps: ['jquery'],
            exports: 'Foundation'
        },
        'foundation.accordion': {
            deps: ['jquery']
        },
        d3: {
            exports: 'd3'
        },
        handlebars: {
            exports: 'Handlebars'
        },
    },

    paths: {
        d3: '../libs/d3/d3',
        jquery: '../libs/jquery/dist/jquery',
        underscore: '../libs/underscore/underscore',
        backbone: '../libs/backbone/backbone',
        foundation: '../libs/foundation/js/foundation.min',
        text: '../libs/requirejs-text/text',
        handlebars: '../libs/handlebars/handlebars.amd'
    }
});

require(['jquery', 'foundation'], function($, Foundation) {
    $(document).foundation();
});

require(['jquery', "backbone", "routers/router"], function($, Backbone, AppRouter) {
    $(document).ready(function() {
        Backbone.history.start();
        var app_router = new AppRouter({silence:true});  // Prevent initial route '' from being invoked
        alert("ready");
    });
});
