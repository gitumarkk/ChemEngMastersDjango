define(["backbone", "models/CSTRModel",
], function(Backbone, CSTRModel){
    var CSTRCollection = Backbone.Model.extend({
        defaults: {},
        model: CSTRModel,
        initialize: function(options){
            this.instanceUrl = options.url;
        },
        url: function(){
            return this.instanceUrl;
        }
    });
    return CSTRCollection;
});
