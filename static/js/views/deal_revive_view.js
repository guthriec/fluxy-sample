/*
 * @author: Ayush
 * @desc: Defines a view that is associated with the DealModel, with 
 *        functionality to revive a deal.
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
      var newDeal = this.model.clone();
      delete newDeal.id;
      delete newDeal.attributes.id;
      console.log(newDeal);
      var oldStart = new Date(newDeal.get('time_start'));
      var oldEnd = new Date(newDeal.get('time_end'));
      var oldStartHours = oldStart.getHours(); 
      var oldStartMinutes = oldStart.getMinutes();
      var oldEndHours = oldEnd.getHours(); 
      var oldEndMinutes = oldEnd.getMinutes();
      var newStart = new Date();
      var newEnd = new Date();
      newStart.setSeconds(0);
      newStart.setMinutes(oldStartMinutes);
      newStart.setHours(oldStartHours); 
      newEnd.setSeconds(0);
      newEnd.setMinutes(oldEndMinutes);
      newEnd.setHours(oldEndHours); 
      newDeal.set('time_start', newStart.toISOString());
      newDeal.set('time_end', newEnd.toISOString());
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
