var app = app || {};

/*
 * @author: Chris
 * Model for a single deal, but restricted to given vendor.
 */
(function() {
  app.VendorDealModel = Backbone.Model.extend({
    initialize: function(vendorId) {
      this.vendorId = vendorId;
      this.urlRoot = '/api/v1/vendors/' + this.vendorId + '/deals/';
      this.set('vendor_id', this.vendorId);
    }
  });
})();
