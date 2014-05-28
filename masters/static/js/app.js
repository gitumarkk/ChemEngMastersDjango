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
            exports: 'Founation'
        },
        'foundation.accordion': {
            deps: ['jquery']
        },
        d3: {
            exports: 'd3'
        }
    },

    paths: {
        d3: 'libs/d3/d3',
        jquery: 'libs/jquery/dist/jquery',
        underscore: 'libs/underscore/underscore',
        backbone: 'libs/backbone/backbone',
        foundation: 'libs/foundation/js/foundation.min',
        // "foundation.accordion" : 'libs/foundation/js/foundation/foundation.accordion',
        text: 'libs/requirejs-text/text'
    }
});

require(['jquery', 'foundation'], function($) {
  $(document).foundation();
});

require(['jquery', "backbone", "routers/router"], function($, Backbone, AppRouter) {
    $(document).ready(function() {
        Backbone.history.start();
        var app_router = new AppRouter();
        alert("ready");
    });
});
