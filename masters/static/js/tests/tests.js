define(["chai", "sinon", "jquery", "views/LayoutView"], function(chai, sinon, $, LayoutView){
    'use strict';

    var assert = chai.assert,
        expect = chai.expect,
        should = chai.should();

    describe('Testing that test runner is set up', function(){
      describe('creating dummy test of: ', function(){
        it('should return -1 when the value is not present', function(){
          assert.equal(-1, [1,2,3].indexOf(5));
          assert.equal(-1, [1,2,3].indexOf(0));
        });
      });
    });

    describe("Testing the layout initializes", function(){
        var layout;
        describe("creating the layout", function(){
            it("should recognize the global ceber object", function(){
                layout = new LayoutView();
            });
        });
    });

});
