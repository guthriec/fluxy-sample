var app = app || {};

(function() {
  app.DealCreateView = Backbone.View.extend({
    setVendor: function(vendorId) {
      this.vendorId = vendorId;
    },

    events: {
      'click .deal-form-submit' : 'postDeal'
    },

    render: function() {
      this.$el.html(_.template($('#dealFormTemplate').html()));
      return this;
    },

    postDeal: function(e) {
      e.preventDefault();
      console.log(this.vendorId);
      var vdModel = new app.VendorDealModel(this.vendorId);
      var $inputs = $('#deal-form :input');
      var values = {};
      $inputs.each(function() {
        values[this.name] = $(this).val();
      });
      vdModel.set("vendor_id", this.vendorId);
      vdModel.set("title", values["title"]);
      vdModel.set("desc", values["desc"]);
      vdModel.set("radius", 5);
      var timeStart = new Date()
      timeStart.setTime(Date.now());
      vdModel.set("time_start", timeStart);
      var minutes = values["minutes"] + 60*values["hours"];
      vdModel.set("time_end", new Date(timeStart.getTime() + minutes*60000));
      console.log(vdModel);
      console.log("trying to post the deal");
      vdModel.save();
      app.router.navigate('view', {trigger: true});
    }
  });
})();
