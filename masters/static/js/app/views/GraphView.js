define(["jquery", "underscore", "backbone", "d3", "views/TableView"],
function($, _, Backbone, d3, TableView){
    'use strict';

    var GraphView = Backbone.View.extend({
        el: "#graph-container",
        template: "",

        initialize: function(options){
            this.rate = options.rate;
            this.reactor = options.reactor;
            this.system = options.system;
            this.src = options.src;

        },

        render: function (){
            var collection, data;
            this.$el.html("");
            if (this.rate === "bioxidation") {
                this.plotGraphBiox(this.src);
            } else if (this.rate === "chemical"){
                this.plotGraphChemical(this.src);
            }

            if (this.reactor === "chemical"){
                this.plotReactorChemical(this.src);
            }
            return this;
        },

        plotGraphBiox : function (src) {
            var graph_container = d3.select(this.el);

            var parent_width = parseInt(graph_container.style('width'), 10);
            var margin = {top: 20, right: 20, bottom: 50, left: 100},
                width = parent_width - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

            var x = d3.scale.log().range([0, width]);
            var y = d3.scale.linear().domain([-5, -5]).range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .ticks(10)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .ticks(5)
                .orient("left");

            var line = d3.svg.line()
                .x(function(d) { return x(d.ferric_ferrous); })
                .y(function(d) { return y(d.rate_ferrous); });

            var svg = graph_container.append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            d3.json(src, function(error, data){
                data.forEach(function(d){
                    d.ferric_ferrous = + d.ferric_ferrous;
                    d.rate_ferrous = + (d.rate_ferrous * 24 * 60 * 60);
                });

                x.domain(d3.extent(data, function(d) { return d.ferric_ferrous; }));
                y.domain(d3.extent(data, function(d) { return d.rate_ferrous; }));

                svg.append("g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + height + ")")
                  .call(xAxis)
                  .append("text")
                  .attr("y", 20)
                  .attr("dy", ".71em")
                  .style("text-anchor", "start")
                  .text("ferric/ferrous ratio");

              svg.append("g")
                  .attr("class", "y axis")
                  .call(yAxis)
                  .append("text")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 6)
                  .attr("dy", ".71em")
                  .style("text-anchor", "end")
                  .text("r_Fe2+");

                  svg.append("path")
                      .datum(data)
                      .attr("class", "line")
                      .attr("d", line);
            });
        },

        plotGraphChemical : function (src) {

            var graph_container = d3.select(this.el);

            var parent_width = parseInt(graph_container.style('width'), 10);
            var margin = {top: 20, right: 20, bottom: 50, left: 100},
                width = parent_width - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

            var x = d3.scale.linear().range([0, width]);
            var y = d3.scale.linear().range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                  .ticks(10)
                    .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                  .ticks(5)
                    .orient("left");

            var line = d3.svg.line()
                .x(function(d) { return x(d.step); })
                  .y(function(d) { return y(d.copper); });

            var svg = graph_container.append("svg")
                .attr("width", width + margin.left + margin.right)
                  .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            d3.json(src, function(error, data){
                data.forEach(function(d){
                    d.copper = + d.copper;
                    d.step = + (d.step / 60);
                });

                x.domain(d3.extent(data, function(d) { return d.step; }));
                y.domain(d3.extent(data, function(d) { return d.copper; }));

                svg.append("g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + height + ")")
                  .call(xAxis)
                  .append("text")
                  .attr("y", 20)
                  .attr("dy", ".71em")
                  .style("text-anchor", "start")
                  .text("Time (min)");

              svg.append("g")
                  .attr("class", "y axis")
                  .call(yAxis)
                  .append("text")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 6)
                  .attr("dy", ".71em")
                  .style("text-anchor", "end")
                  .text("[Copper]");

                  svg.append("path")
                      .datum(data)
                      .attr("class", "line")
                      .attr("d", line);
            });
        },

        plotReactorChemical : function (src) {
            var x_variable, y_variable;

            var graph_container = d3.select(this.el);

            var parent_width = parseInt(graph_container.style('width'), 10);
            var margin = {top: 20, right: 20, bottom: 50, left: 100},
                width = parent_width - margin.left - margin.right,
                height = 500 - margin.top - margin.bottom;

            var x = d3.scale.linear().range([0, width]);
            var y = d3.scale.linear().range([height, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .ticks(10)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .ticks(5)
                .orient("left");

            var metal = d3.svg.line()
                .x(function(d) { return x(d.x); })
                .y(function(d) { return y(d.metal); });

            var ferrous_out = d3.svg.line()
                .x(function(d) { return x(d.x); })
                .y(function(d) { return y(d.ferrous_out); });

            var rate_ferrous = d3.svg.line()
                .x(function(d) { return x(d.x); })
                .y(function(d) { return y(d.rate_ferrous); });

            var svg = graph_container.append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            d3.json(src, function(error, data){
              data.forEach(function(d){
                  d.x = + d.step / 60 ;
                  d.metal = + d.cstr_data.components.Cu.component_moles;
                  d.rate_ferrous = + d.cstr_data.components.Cu.rate_ferrous;
                  d.ferrous_out = + d.flow_out.components.ferrous;
              });
                // new TableView({data: data});

                x.domain(d3.extent(data, function(d) { return d.x; }));
                y.domain(d3.extent(data, function(d) { return d.metal; }));

                svg.append("path")
                      .datum(data)
                      .attr("class", "line")
                      .attr("d", metal);

                svg.append("g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + height + ")")
                  .call(xAxis)
                  .append("text")
                  .attr("y", 20)
                  .attr("dy", ".71em")
                  .style("text-anchor", "start")
                  .text("Time (s)");

                svg.append("g")
                  .attr("class", "y axis")
                  .call(yAxis)
                  .append("text")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 6)
                  .attr("dy", ".71em")
                  .style("text-anchor", "end")
                  .text("[Copper mol/l]");

                var svg_2 = graph_container.append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                y.domain(d3.extent(data, function(d) { return d.ferrous_out; }));

                svg_2.append("path")
                      .datum(data)
                      .attr("class", "line")
                      .style("stroke", "red")
                      .attr("d", ferrous_out);

                svg_2.append("g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + height + ")")
                  .call(xAxis)
                  .append("text")
                  .attr("y", 20)
                  .attr("dy", ".71em")
                  .style("text-anchor", "start")
                  .text("Time (s)");

                svg_2.append("g")
                  .attr("class", "y axis")
                  .call(yAxis)
                  .append("text")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 6)
                  .attr("dy", ".71em")
                  .style("text-anchor", "end")
                  .text("[Ferrous Concentration mol/l]");

                var svg_3 = graph_container.append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                    .append("g")
                    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

                y.domain(d3.extent(data, function(d) { return d.rate_ferrous; }));

                svg_3.append("path")
                      .datum(data)
                      .attr("class", "line")
                      .style("stroke", "red")
                      .attr("d", rate_ferrous);

                svg_3.append("g")
                  .attr("class", "x axis")
                  .attr("transform", "translate(0," + height + ")")
                  .call(xAxis)
                  .append("text")
                  .attr("y", 20)
                  .attr("dy", ".71em")
                  .style("text-anchor", "start")
                  .text("Time (s)");

                svg_3.append("g")
                  .attr("class", "y axis")
                  .call(yAxis)
                  .append("text")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 6)
                  .attr("dy", ".71em")
                  .style("text-anchor", "end")
                  .text("Rate Ferrous");
            });
        }
    });

    return GraphView;
});
