var app = app || {};

$(function () {
  app.router = new app.DashboardRouter();
  app.currentVendor = 1;
  Backbone.history.start();
});
