/*
 * @author: Ayush, Chris
 * @desc: Defines the model that represents the deal that is going to be
 * displayed.
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
      } else {
        deal = resp;
      }
      deal.photo = new PhotoModel(deal.photo);
      return deal;
    }
  });
  return DealModel; 
});
