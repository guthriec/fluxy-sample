define([
  'backbone',
  'marionette',
  'underscore',
  'views/left_nav_view',
  'collections/deals_collection',
  'collections/photos_collection',
  'layouts/main_content_layout',
  'layouts/modal_content_layout'
], function(Backbone, Marionette, _, LeftNavView, DealsCollection,
  PhotosCollection, MainContentLayout, ModalContentLayout) {

  // Start the dashboard Marionette/Backbone app
  var DashboardApp = new Marionette.Application();

  // Register the main dashboard region
  DashboardApp.addRegions({
    dashboardRegion: '#dashboard-container',
    leftNavbarRegion: '#left-navbar-container',
    modalRegion: '#modal-container'
  }),

  DashboardApp.addInitializer(function(options) {
    var leftNavView = new LeftNavView();
    DashboardApp.leftNavbarRegion.show(leftNavView);
  });

  // Load the initializer
  DashboardApp.addInitializer(function(options) {
    var mainOpts = {};
    mainOpts.deals = new DealsCollection([], { 'vendorId': vendorId,
                                           'listenForChanges': true });
    mainOpts.deals.fetch({ reset: true });

    var mainContent = new MainContentLayout(mainOpts);
    DashboardApp.dashboardRegion.show(mainContent);

    var modalOpts = {};
    modalOpts.photos = new PhotosCollection([], { 'vendorId': vendorId });
    modalOpts.photos.fetch({ reset: true });

    var modalContent = new ModalContentLayout(modalOpts);
    DashboardApp.modalRegion.show(modalContent);
  });

  return DashboardApp;
});
