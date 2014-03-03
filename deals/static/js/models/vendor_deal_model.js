var app = app || {};

(function() {
  app.VendorDealModel = Backbone.Model.extend({
    initialize: function(vendorId) {
      this.vendorId = vendorId;
      this.urlRoot = '/api/v1/vendors/' + this.vendorId + '/deals/';
      this.set('vendor_id', this.vendorId);
    }
  });
})();
