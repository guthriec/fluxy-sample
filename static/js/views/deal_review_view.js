/*
 * @author: Ayush
 * @desc: Defines the view that is associated with the DealModel. It represents
 * a DealModel as a <tr> tag.
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
      return data;
    }
  });
  return DealReviewView;
});
