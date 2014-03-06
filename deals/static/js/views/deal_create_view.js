var app = app || {};

/*
 * @author: Chris
 * View for a vendor to fill in a deal form and create a new deal
 */
(function(window, document, undefined) {
  app.DealCreateView = Backbone.View.extend({
    // View creator should know the vendorId. This may eventually be moved
    // to be a property of app.
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

    /*
     * postDeal() reads the input data from deal-form and constructs a
     * VendorDealModel object.
     */
    postDeal: function(e) {
      e.preventDefault();
      var vdModel = new app.VendorDealModel(this.vendorId);
      var $inputs = $('#deal-form :input');
      var values = {};
      $inputs.each(function() {
        values[this.name] = $(this).val();
      });
      //vdModel.set("vendor_id", this.vendorId);
      vdModel.set("title", values["title"]);
      vdModel.set("desc", values["desc"]);
      vdModel.set("radius", 5);

      // For now the client performs the logic to find the "now" time and
      // convert duration in hours and minutes to an end time. This should
      // eventually be moved to the server.
      var timeStart = new Date()
      timeStart.setTime(Date.now());
      vdModel.set("time_start", timeStart);
      var minutes = values["minutes"] + 60*values["hours"];
      vdModel.set("time_end", new Date(timeStart.getTime() + minutes*60000));

      // Post the model and redirect to a view of all the vendor's deals.
      vdModel.save();
      app.router.navigate('view', {trigger: true});
    }
  });
})(this, this.document);
