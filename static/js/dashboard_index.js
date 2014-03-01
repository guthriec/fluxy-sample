var DashboardIndexView = Backbone.View.extend({
  render: function() {
    var template = _.template($("#dashIndexTemplate").html());
    this.$el.html(template);
    return this;
  }
});
