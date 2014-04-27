/*
 * @author: Ayush
 * @desc: Responsible for rendering and displaying any necessary modals.
 */
define([
  'marionette',
  'vent',
  'bootstrap'
], function(Marionette, vent, Bootstrap) {
  var ModalControllerView = Marionette.ItemView.extend({
    template: '#modal-controller-template',

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

      $modal.find('#title td:nth-child(2)').html(deal.title);
      $modal.find('#description td:nth-child(2)').html(deal.desc);

      var d = Math.abs((new Date(deal.time_start)) - (new Date(deal.time_end)));
      var hours = parseInt(d / 3600000);
      var minutes = d % 3600000 / 60000;
      $modal.find('#duration td:nth-child(2)').html(hours + 'H ' + 
                                                    minutes + 'M');

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
