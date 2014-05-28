define(["backbone"],
function(Backbone){
    var TableView = Backbone.View.extend({
        template: "#draw-table",
        el: "#graph-data",
        initialize: function(options){
            this.data = options.data;
            this.render();
        },
        render: function(){
            var tpl = _.template($(this.template).html(), {data: this.data});
            this.$el.html(tpl);
            return this;
        }
    });
    return TableView;
});
