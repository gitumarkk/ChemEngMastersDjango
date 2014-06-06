define(["d3"], function(d3){
    return {
        graph_container: function(el){
            console.log("graph container");
            this.graph_container = d3.select(el);

            this.parent_width = parseInt(this.graph_container.style('width'), 10);
            this.margin = {top: 20, right: 20, bottom: 50, left: 100};
            this.width = this.parent_width - this.margin.left - this.margin.right;
            this.height = 500 - this.margin.top - this.margin.bottom;

            this.x = d3.scale.log().range([0, this.width]);
            this.y = d3.scale.linear().domain([-5, -5]).range([this.height, 0]);

            this.xAxis = d3.svg.axis()
                .scale(this.x)
                .ticks(10)
                .orient("bottom");

            this.yAxis = d3.svg.axis()
                .scale(this.y)
                .ticks(5)
                .orient("left");

            this.line = d3.svg.line()
                .x(function(d) { return x(d.ferric_ferrous); })
                .y(function(d) { return y(d.rate_ferrous); });

            this.svg = this.graph_container.append("svg")
                .attr("width", this.width + this.margin.left + this.margin.right)
                .attr("height", this.height + this.margin.top + this.margin.bottom)
                .append("g")
                .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
        },

        add_ferrous_data: function(ferrous_data){

        },

        add_ferric_data: function (ferric_data){

        },

        append_copper: function(copper_data){

        },

        append_cupric: function(cupric_data){

        }
    };
});
