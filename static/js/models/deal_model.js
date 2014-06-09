/*
 * @author: Ayush, Chris
 * @desc: The model that represents a single deal. Parses the API response
 * for a single deal, creating as appropriate a nested photo model instance.
 */
define([
 'backbone',
 'models/photo_model'
], function(Backbone, PhotoModel) {
  var DealModel = Backbone.Model.extend({
    parse: function(resp) {
      var deal = {};
      if (resp.hasOwnProperty('data')) {
        deal = resp.data;
        if (deal.length > 0) // meaning deal is an array
          deal = deal[0];
      } else {
        deal = resp;
      }
      deal.photo = new PhotoModel(deal.photo);
      return deal;
    }
  });
  return DealModel;
});
