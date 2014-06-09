/*
 * @author: Chris
 * @desc: Defines the model that represents user feedback 
 */
define([
 'backbone'
], function(Backbone) {
  var FeedbackModel = Backbone.Model.extend({
    url: '/api/v1/feedback/',
  });
  return FeedbackModel; 
});