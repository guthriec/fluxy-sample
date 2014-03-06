var app = app || {};

(function(window, document, undefined) {
  var DealRowView = Backbone.View.extend({
    tagName: "tr",

    initialize: function(deal) {
      this.deal = deal;
    },

    render: function() {
      var template = _.template($('#dealsRowTemplate').html(), this.deal.toJSON());
      this.$el.html(template);
      return this;
    }
  });
})(this, this.document);
