/*
 * @author: Ayush, Chris
 * @desc: Defines the model that represents the deal that is going to be
 * displayed.
 */
define([
 'backbone'
], function(Backbone) {
  var FeedbackModel = Backbone.Model.extend({
    url: '/api/v1/feedback/',
  });
  return FeedbackModel; 
});
