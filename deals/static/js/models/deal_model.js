var VendorDealModel = Backbone.Model.extend({
  initialize: function(vendorId) {
    this.vendorId = vendorId;
  },
  urlRoot: '/api/v1/vendors/',
  url: function() {
    return this.urlRoot + this.vendorId + '/deals/' + this.id;
  },
  defaults: {
    vendor_id: this.vendorId,
    vendor: new VendorModel(this.vendorId),
    title: "",
    desc: "",
    radius: -1,
    time_start: new Date(),
    time_end: new Date()
  },
  parse: function(response) {
    var embeddedVendor = response['vendor'];
    response['vendor'] = new VendorModel(embeddedVendor, {parse:true});
    return response;
  }
});

