var app = app || {};

/*
 * @author: Chris
 * Not used now, will be useful for the user webapp.
 */
(function(window, document, undefined) {
  app.DealModel= Backbone.Model.extend({
    urlRoot: '/api/v1/deals/';

    parse: function(response) {
      var embeddedVendor = response['vendor'];
      response['vendor'] = new app.VendorModel(embeddedVendor, {parse:true});
      return response;
    }
  });
})(this, this.document);
