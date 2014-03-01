var app = app || {};

(function() {
  app.VendorModel = Backbone.Model.extend({
    initialize: function(vendorId) {
      this.id = vendorId;
    },
    urlRoot: '/api/v1/vendors/',
    url: function() {
      return this.urlRoot + this.id;
    },
    defaults: {
      name: "",
      address: "",
      businessType: "",
      latitude: -1,
      longitude: -1,
      webUrl: "",
      yelpUrl: "",
    }
  });
})();
