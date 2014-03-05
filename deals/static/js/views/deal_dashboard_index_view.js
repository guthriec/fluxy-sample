var app = app || {};

/*
 * @author: Chris
 * Home view for the dashboard application.
 */
(function() {
  app.DashboardIndexView = Backbone.View.extend({
    render: function() {
      var template = _.template($("#dashIndexTemplate").html());
      this.$el.html(template);
      return this;
    }
  });
})();
