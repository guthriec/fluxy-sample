var app = app || {};

(function() {
  app.VendorDealModel = Backbone.Model.extend({
    initialize: function(vendorId) {
      this.vendorId = vendorId;
    },
    urlRoot: '/api/v1/vendors/' + this.vendorId + '/deals/',
    defaults: {
      vendor_id: this.vendorId,
      vendor: new app.VendorModel(this.vendorId),
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
