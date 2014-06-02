/*
 * @author: Chris, Ayush
 * @desc: a Marionette layout that wraps the main content of the dashboard.
 *        Expects to be initalized with a complete set of collections for
 *        every dashboard view. Handles navigation within the dashboard.
 */
define([
  'marionette',
  'vent',
  'views/active_deals_collection_view',
  'views/deal_create_form_view',
  'views/revive_deals_collection_view',
  'views/review_collection_view',
  'views/feedback_view'
], function(Marionette, vent, ActiveCollectionView, DealCreateFormView,
            ReviveCollectionView, ReviewCollectionView, FeedbackView) {
  var MainContentLayout = Marionette.Layout.extend({
    template: "#main-content-template",

    regions: {
      dashboard: '#dashboard'
    },

    initialize: function(options) {
      vent.on('showCreateView', this.showCreate, this);
      vent.on('showReviveView', this.showRevive, this);
      vent.on('showReviewView', this.showReview, this);
      vent.on('showActiveView', this.showActive, this);
      vent.on('showFeedbackView', this.showFeedback, this);

      this.deals = options.deals;
      this.scheduledDeals = this.deals.scheduledCollection();
      this.expiredDeals = this.deals.expiredCollection();
      this.activeDeals = this.deals.activeCollection();
      this.activeDealsCollectionView = new ActiveCollectionView({
        collection: this.activeDeals
      });
      this.reviewCollectionView = new ReviewCollectionView({
        collection: this.scheduledDeals
      });
      this.reviveDealsView = new ReviveCollectionView({
        collection: this.expiredDeals
      });
      this.dealCreateForm = new DealCreateFormView();
      this.feedbackView = new FeedbackView();
    },


    showCreate: function(deal) {
      if (deal)
        this.dealCreateForm.setDeal(deal);
      this.dashboard.show(this.dealCreateForm);
    },

    showRevive: function() {
      this.dashboard.show(this.reviveDealsView);
    },

    showReview: function() {
      this.dashboard.show(this.reviewCollectionView);
    },

    showActive: function() {
      this.dashboard.show(this.activeDealsCollectionView);
    },

    showFeedback: function() {
      this.dashboard.show(this.feedbackView);
    },

    onShow: function() {
      this.dashboard.show(this.dealCreateForm);
    },
  });
  return MainContentLayout;
});
