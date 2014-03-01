var VendorModel = Backbone.Model.extend({
  initialize: function(vendor_id) {
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

