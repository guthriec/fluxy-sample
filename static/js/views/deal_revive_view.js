/*
 * @author: Ayush
 * @desc: Defines a view that is associated with the DealModel, with 
 *        functionality to revive a deal.
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
      Vent.trigger('showCreateView', this.model);
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
