/*
 * @author: Chris
 * @desc: Initializes the marionette application. Defines regions for the main
 * content, the modal content, and the left navbar. 
 */

define([
  'backbone',
  'marionette',
  'underscore',
  'consumer_deals/layouts/main_content_layout',
  'consumer_deals/layouts/modal_content_layout'
], function(Backbone, Marionette, _, MainContentLayout, ModalContentLayout) {

  // Start the deals Marionette/Backbone app
  var DealsApp = new Marionette.Application();

  // Register the main regions
  DealsApp.addRegions({
    dealsRegion: '#deals-container',
    leftNavbarRegion: '#left-navbar-container',
    modalRegion: '#modal-container'
  }),

  DealsApp.addInitializer(function(options) {
    //var leftNavView = new LeftNavView();
    //DashboardApp.leftNavbarRegion.show(leftNavView);
  });

  // Load the initializer
  DealsApp.addInitializer(function(options) {
    var mainOpts = {};
    var mainContent = new MainContentLayout(mainOpts);
    DealsApp.dealsRegion.show(mainContent);
    var modalOpts = {};
    var modalContent = new ModalContentLayout(modalOpts);
    DealsApp.modalRegion.show(modalContent);
    /* mainOpts.deals = new DealsCollection([], { 'vendorId': vendorId,
                                           'listenForChanges': true });
    mainOpts.deals.fetch({ reset: true });

    var mainContent = new MainContentLayout(mainOpts);
    DashboardApp.dashboardRegion.show(mainContent);

    modalOpts.photos = new PhotosCollection([], { 'vendorId': vendorId });
    modalOpts.photos.fetch({ reset: true });
    */
  });

  return DealsApp;
});
