require.config({
    baseUrl: '../app',
    paths: {
        // 'jquery' : '../vendor/jquery.min',
        'mocha' : '../node_modules/mocha/mocha',
        'chai' : '../node_modules/chai/chai',
        'sinon' : '../node_modules/sinon/pkg/sinon',
        'ceber': 'app'
    },


     shim: {
        'sinon': {
            exports: 'sinon'
        }
    }
});

require(['require', 'mocha', 'ceber'], function(require){
    mocha.setup('bdd');
    require(['tests.js'], function() {
        if (window.mochaPhantomJS) {
            mochaPhantomJS.run();
        } else {
            mocha.run();
        }
    });
});
