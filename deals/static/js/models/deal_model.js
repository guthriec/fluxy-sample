var app = app || {};

(function() {
  app.DealModel= Backbone.Model.extend({
    urlRoot: '/api/v1/deals/';

    parse: function(response) {
      var embeddedVendor = response['vendor'];
      response['vendor'] = new app.VendorModel(embeddedVendor, {parse:true});
      return response;
    }
  });
})();
