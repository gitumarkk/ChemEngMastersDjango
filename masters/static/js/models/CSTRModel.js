define(["backbone",
], function(Backbone){
    var CSTRModel = Backbone.Model.extend({
        defaults: {},
        initialize: function(options){
            this.instanceUrl = options.url;
        },
        url: function(){
            return this.instanceUrl;
        }
    });
    return CSTRModel;
});
