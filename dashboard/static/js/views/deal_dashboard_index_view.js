var app = app || {};

/*
 * @author: Chris
 * Home view for the dashboard application.
 */
(function(window, document, undefined) {
  app.DashboardIndexView = Backbone.View.extend({
    render: function() {
      var template = _.template($("#dashIndexTemplate").html());
      this.$el.html(template);
      return this;
    }
  });
})(this, this.document);
