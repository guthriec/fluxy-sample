var DealModel = Backbone.Model.extend({
  urlRoot: '/api/v1/deals',
  defaults: {
    vendor_id: -1,
    title: "",
    desc: "",
    radius: 5
  }
});

var DealCollection = Backbone.Collection.extend({
  model: DealModel
});
