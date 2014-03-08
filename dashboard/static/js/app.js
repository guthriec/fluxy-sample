var app = app || {};

// Initialize the app
$(function () {
  app.router = new app.DashboardRouter();
  Backbone.history.start();
});
