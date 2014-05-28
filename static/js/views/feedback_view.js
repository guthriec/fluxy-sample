/*
 * @author: Chris
 * @desc: Defines the view that's responsible for rendering the feedback
 *        form and submitting it. 
 */
define([
  'marionette',
  'models/feedback_model'
], function(Marionette, FeedbackModel) {
  var FeedbackView = Marionette.ItemView.extend({

    template: '#contact-form-template',
   
    initialize: function() {
      this.model = new FeedbackModel();
    },

    events: {
      'click #submit-btn': 'sendFeedback'
    },

    sendFeedback: function(e) {
      e.preventDefault();
      this.model.set({'message': this.$el.find('#feedback').val()});
      this.model.save();
      this.$el.find('#submit-btn').blur();
    },

  });
  return FeedbackView;
});
