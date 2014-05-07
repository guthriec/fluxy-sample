/*
 * @author: Chris 
 * @desc: Responsible for rendering and displaying revive deal modal.
 */
define([
  'marionette',
  'vent',
  'bootstrap',
  'fluxy_time'
], function(Marionette, vent, Bootstrap, FluxyTime) {
  var ModalControllerView = Marionette.ItemView.extend({
    template: '#revive-deal-modal-template',

    events: {
      'click #revive-deal-modal #submit-btn': 'reviveDeal',
      'click #revive-deal-modal #cancel-btn': 'cancelReviveDeal'
    },

    initialize: function() {
      console.log('initialized');
      vent.on('reviveDealModalTrigger', this.showReviveModal, this);
    },

    showReviveModal: function(deal) {
      console.log('reviveDealModalTrigger triggered');
      this.newDeal = deal;
      var $modal = this.$el.find('#revive-deal-modal');
      $modal.modal('show');
    },

    confirmDealCreation: function(deal) {
      this.newDeal = deal;

      var $modal = this.$el.find('#create-deal-modal');

      $modal.find('#create-title-cell').html(deal.title);
      $modal.find('#create-extra-info-cell').html(deal.desc);
      if (deal.max_deals > 0) {
        $modal.find('#create-max-deals-cell').html(deal.max_deals);
      } else {
        $modal.find('#create-max-deals-cell').html("Unlimited");
      }
      var timeStart = new Date(deal.time_start);
      var timeEnd = new Date(deal.time_end);
      $modal.find('#create-start-time-cell').html(FluxyTime.getDateString(
                                                            timeStart)) 
      $modal.find('#create-end-time-cell').html(FluxyTime.getDateString(
                                                             timeEnd));
      var d = Math.abs((new Date(deal.time_start)) - (new Date(deal.time_end)));
      var hours = parseInt(d / 3600000);
      var minutes = d % 3600000 / 60000;

      $modal.modal('show');
    },

    cancelCreateDeal: function() {
      // TODO: send trigger to clear form
      this.$el.find('#create-deal-modal').modal('hide');
    },

    createDeal: function() {
      // TODO: send trigger to clear from
      vent.trigger('createDealTrigger', this.newDeal);
      this.$el.find('#create-deal-modal').modal('hide');
    }
  });

  return ModalControllerView;
});
