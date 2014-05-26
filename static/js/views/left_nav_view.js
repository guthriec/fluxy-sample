define([
  'marionette',
  'vent'
], function(Marionette, vent) {
  var LeftNavView = Marionette.ItemView.extend({
    tagName: 'ul',
    className: 'nav nav-stacked list-group',
    id: 'left-navbar',
    template: '#left-navbar-template',

    initialize: function(options) {
      vent.on('showCreateView', this.switchCreate, this);
      vent.on('showReviveView', this.switchRevive, this);
      vent.on('showReviewView', this.switchReview, this);
      vent.on('showActiveView', this.switchActive, this);
    },

    events: {
      'click #nav-create': 'showCreate',
      'click #nav-revive': 'showRevive',
      'click #nav-review': 'showReview',
      'click #nav-active': 'showActive'
    },

    showCreate: function(e) {
      e.preventDefault();
      vent.trigger('showCreateView');
    },

    switchCreate: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-create").addClass("selected");
    },

    showRevive: function(e) {
      e.preventDefault();
      vent.trigger('showReviveView');
    },

    switchRevive: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-revive").addClass("selected");
    },

    showReview: function(e) {
      e.preventDefault();
      vent.trigger('showReviewView');
    },

    switchReview: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-review").addClass("selected");
    },

    showActive: function(e) {
      e.preventDefault();
      vent.trigger('showActiveView');
    },

    switchActive: function(e) {
      $("#left-navbar").find(".list-group-item").removeClass("selected");
      $("#nav-active").addClass("selected");
    },

    onShow: function() {
      $("#nav-create").addClass("selected");
    }
  });
  return LeftNavView;
});
