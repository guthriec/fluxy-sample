VendorApp = new Backbone.Marionette.Application();

VendorApp.addRegions({
  vendorFormRegion: '#vendor-form'
});

VendorFormView = Backbone.Marionette.ItemView.extend({
  events: {
    'click #submit-btn': 'editVendor',
  },
  template: "#vendor-edit-form-template",

  render: function() {
    this.$el.html(_.template($(this.template).html()));
    return this;
  },

  editVendor: function(e) {
    e.preventDefault();

    var $formInputs = $('#vendor-form :input');
    var formData = new FormData();

    var reader = new FileReader();
    var imageIndex = -1;

    console.log($formInputs);
    $formInputs.each(function(index) {
      if (this.name != 'image')
        formData.append(this.name, $(this).val());
      else
        imageIndex = index;
    });

    function submitRequest(formData) {
      $.ajax({
        url: '/api/v1/vendor/1/',
        type: 'PUT',
        contentType: false,
        data: formData,
        processData: false
      });
      /*
      var request = new XMLHttpRequest();
      request.open('PUT', '/api/v1/vendor/1/');
      request.send(formData);
      */
    };

    if ($formInputs[imageIndex].files.length > 0) {
      reader.readAsArrayBuffer($formInputs[imageIndex].files[0]);
      reader.onload = function(evt) {
        console.log('foo');
        formData.append('image', evt.target.result);
        submitRequest(formData);
      };
    } else {
      submitRequest(formData);
    }

    this.$el.find('#submit-btn').blur();
  },
});

VendorApp.addInitializer(function(options) {
  VendorApp.events = _.extend({}, Backbone.Events);

  var vendorForm = new VendorFormView();
  VendorApp.vendorFormRegion.show(vendorForm);
});

$(document).ready(function() {
  VendorApp.start();
});
