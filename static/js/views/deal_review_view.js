/*
 * @author: Chris
 * @desc: Defines the view that's responsible for rendering a single deal
 *        for review. It includes functionality for the Cancel Deal button.
 */
define([
  'marionette',
  'fluxy_time',
  'vent'
], function(Marionette, FluxyTime, Vent) {
  var DealReviewView = Marionette.ItemView.extend({

    template: '#review-deal-template',
    
    tagName: 'tr',
    
    className: 'deal',
    
    events: {
      'click .cancel-btn': 'cancelDeal'
    },

    cancelDeal: function(e) {
      e.preventDefault();
      Vent.trigger('cancelDealTrigger', this.model);
      this.$el.find('.cancel-btn').blur();
    },

    serializeData: function() {
      var data = this.model.toJSON();
      var start_date = new Date(data.time_start);
      var end_date = new Date(data.time_end);
      data.pretty_time_start = FluxyTime.getDateStringHTML(start_date); 
      data.pretty_time_end = FluxyTime.getDateStringHTML(end_date);
      if (data.max_deals == -1) {
        data.max_deals = "Unlimited";
      }
      return data;
    }
  });
  return DealReviewView;
});
