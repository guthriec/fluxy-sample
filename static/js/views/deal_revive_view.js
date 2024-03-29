/*
 * @author: Chris
 * @desc: The view for a single expired deal that can be revived. Includes
 * functionality for the Revive Deal button, including sending the user to the
 * appropriately populated create view. Serializes a deal model for display
 * (interpreting max deals and deals remaining, and serializing the dates to
 * human-readable HTML).
 */
define([
  'marionette',
  'models/deal_model',
  'fluxy_time',
  'vent'
], function(Marionette, DealModel, FluxyTime, Vent) {
  var DealReviveView = Marionette.ItemView.extend({

    template: '#revive-deal-template',
    
    tagName: 'tr',
    
    className: 'deal',
    
    events: {
      'click .revive-btn': 'reviveDeal'
    },

    reviveDeal: function(e) {
      e.preventDefault();

      var oldStart = new Date(this.model.get('time_start'));
      var oldEnd = new Date(this.model.get('time_end'));
      var newStart = FluxyTime.sameTimeToday(oldStart);
      var newEnd = FluxyTime.sameTimeToday(oldEnd);
      // We only copy the attributes we need
      var newDeal = new DealModel({
        'title': this.model.get('title'),
        'subtitle': this.model.get('subtitle'),
        'desc': this.model.get('desc'),
        'max_deals': this.model.get('max_deals'),
        'photo': this.model.get('photo'),
        'time_start': newStart.toISOString(),
        'time_end': newEnd.toISOString(),   
      });
      Vent.trigger('showCreateView', newDeal);
      this.$el.find('.revive-btn').blur();
    },

    serializeData: function() {
      var data = this.model.toJSON();
      var start_date = new Date(data.time_start);
      data.pretty_time_start = FluxyTime.getDateStringHTML(start_date);
      data.photo = data.photo.attributes;
      return data;
    }
  });
  return DealReviveView;
});
