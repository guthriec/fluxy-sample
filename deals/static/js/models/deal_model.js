var app = app || {};

(function() {
  app.VendorDealModel = Backbone.Model.extend({
    initialize: function(vendorId) {
      this.vendorId = vendorId;
      this.urlRoot = '/api/v1/vendors/' + this.vendorId + '/deals/';
      this.defaults.vendor_id = this.vendorId;
      this.defaults.vendor = new app.VendorModel(this.vendorId);
    },

    defaults: {
      title: "",
      desc: "",
      radius: -1,
      time_start: new Date(),
      time_end: new Date()
    },

    parse: function(response) {
      var embeddedVendor = response['vendor'];
      response['vendor'] = new app.VendorModel(embeddedVendor, {parse:true});
      return response;
    }
  });
})();
