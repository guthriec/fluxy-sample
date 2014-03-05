var app = app || {};

/*
 * @author: Chris
 * Model for vendor data.
 */
(function() {
  app.VendorModel = Backbone.Model.extend({
    initialize: function(vendorId) {
      this.id = vendorId;
    },
    urlRoot: '/api/v1/vendors/',
    url: function() {
      return this.urlRoot + this.id;
    }
  });
})();
