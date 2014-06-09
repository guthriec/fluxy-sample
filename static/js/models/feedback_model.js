/*
 * @author: Chris
 * @desc: The model that represents user feedback. Specifies the API URL.
 */
define([
 'backbone'
], function(Backbone) {
  var FeedbackModel = Backbone.Model.extend({
    url: '/api/v1/feedback/',
  });
  return FeedbackModel; 
});
