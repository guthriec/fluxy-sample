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
  var DealReviveView = Marionette.ItemView.extend({

    template: '#revive-deal-template',
    
    tagName: 'tr',
    
    className: 'deal',
    
    events: {
      'click .revive-btn': 'reviveDeal'
    },

    reviveDeal: function(e) {
      e.preventDefault();
      Vent.trigger('reviveDealTrigger', this.model);
      this.$el.find('.revive-btn').blur();
    },

    serializeData: function() {
      var data = this.model.toJSON();
      var start_date = new Date(data.time_start);
      data.pretty_time_start = FluxyTime.getDateStringHTML(start_date); 
      return data;
    }
  });
  return DealReviveView;
});
