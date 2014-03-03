var app = app || {};

(function() {
  app.RegView = Backbone.View.extend({
    events: {
      'click .reg-form-submit' : 'register'
    },

    render: function() {
      var template = _.template($('#regTemplate').html());
      this.$el.html(template);
      return this;
    },

    register: function(e) {
      e.preventDefault();
      this.model = new app.RegModel();
      var $inputs = $('#reg-form :input');
      var values = {}
      $inputs.each(function() {
        values[this.name] = $(this).val();
      });
      var self = this;
      if (values['confirm-password'] != values['password']) {
        app.error = "Passwords do not match";
        self.render();
      }
      this.model.save(values, {
        success: function(model, response) {
          app.router.navigate('', {trigger: true}); 
        },
        error: function(model, response) {
          app.error = "Invalid login";
          self.render();
        }
      });
    }
  });
})();
