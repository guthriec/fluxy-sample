var app = app || {};

$(function () {
  app.router = new app.DashboardRouter();
  Backbone.history.start();
});
