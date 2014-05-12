/*
 * @author: Ayush, Chris
 * @desc: Defines the model that represents the deal that is going to be
 * displayed.
 */
define([
 'backbone'
], function(Backbone) {
  var DealModel = Backbone.Model.extend({
    parse: function(resp) {
      if (resp.hasOwnProperty('data')) {
        return resp.data;
      } else {
        return resp;
      }
    }
  });
  return DealModel; 
});
