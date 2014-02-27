var DealRowView = Backbone.View.extend({
  tagName: "tr",

  initialize: function(deal) {
    this.deal = deal;
  }
});
