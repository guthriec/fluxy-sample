define([
  'backbone',
  'marionette',
  'underscore',
  'views/modal_controller_view',
  'views/left_nav_view',
  'collections/deals_collection',
  'layouts/main_content_layout'
], function(Backbone, Marionette, _, ModalControllerView, LeftNavView,
            DealsCollection, MainContentLayout) {

  // Start the dashboard Marionette/Backbone app
  var DashboardApp = new Marionette.Application();

  // Add the events initializer first
  DashboardApp.addInitializer(function(options) {
    DashboardApp.events = _.extend({}, Backbone.Events);
  });

  // Register the main dashboard region
  DashboardApp.addRegions({
    dashboardRegion: '#dashboard-container',
    leftNavbarRegion: '#left-navbar-container',
    modalRegion: '#modal-container'
  }),

  DashboardApp.addInitializer(function(options) {
    var modalControllerView = new ModalControllerView();
    DashboardApp.modalRegion.show(modalControllerView);
  });

  DashboardApp.addInitializer(function(options) {
    var leftNavView = new LeftNavView();
    DashboardApp.leftNavbarRegion.show(leftNavView);
  });

  // Load the initializer
  DashboardApp.addInitializer(function(options) {
    var opts = {};
    opts.deals = new DealsCollection([], { 'vendorId': vendorId, 'listenForCreate': true });
    opts.deals.fetch({ reset: true });

    var mainContent = new MainContentLayout(opts);
    DashboardApp.dashboardRegion.show(mainContent);
  });

  return DashboardApp;
});
