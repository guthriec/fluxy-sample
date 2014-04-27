/*
 * @author: Ayush
 * @desc: Responsible for rendering and displaying any necessary modals.
 */
define([
  'marionette',
  'vent',
  'bootstrap',
  'fluxy_time'
], function(Marionette, vent, Bootstrap, FluxyTime) {
  var ModalControllerView = Marionette.ItemView.extend({
    template: '#create-deal-modal-template',

    events: {
      'click #create-deal-modal #create-btn': 'createDeal',
      'click #create-deal-modal #cancel-btn': 'cancelCreateDeal'
    },

    initialize: function() {
      vent.on('createDealConfirmTrigger', this.confirmDealCreation, this);
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
      $modal.find('#create-start-time-cell').html(FluxyTime.getDateString(
                                                             deal.time_start));
      $modal.find('#create-end-time-cell').html(FluxyTime.getDateString(
                                                             deal.time_end));
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
