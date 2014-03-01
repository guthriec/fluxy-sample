var VendorDealModel = Backbone.Model.extend({
  urlRoot: '/api/v1/vendors/',
  url: function() {
    return this.urlRoot + this.vendor_id + '/deals/' + this.id;
  },
  defaults: {
    vendor_id: -1,
    title: "",
    desc: "",
    radius: 5
  }
});

