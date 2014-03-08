var app = app || {};

/*
 * @author: Chris
 * Collection of VendorDealModels. Pretty bad interface, works but will
 * be redesigned.
 */
(function(window, document, undefined) {
  app.VendorDealCollection = Backbone.Collection.extend({
    initialize: function() {
      this.vendor_id = -1;
    },
    urlRoot: '/api/v1/vendors/',
    model: app.VendorDealModel,
    url: function() {
      return this.urlRoot + this.vendor_id + '/deals/';
    },
    set_vendor: function(v_id) {
      this.vendor_id = v_id;
    }
  });
})(this, this.document);
