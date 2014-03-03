var app = app || {};

(function() {
  app.AuthView = Backbone.View.extend({
    events: {
      'click .auth-form-submit' : 'authenticate'
    },

    render: function() {
      var template = _.template($('#authTemplate').html());
      this.$el.html(template);
      return this;
    },

    authenticate: function(e) {
      e.preventDefault();
      this.model = new app.AuthModel();
      var $inputs = $('#auth-form :input');
      var values = {}
      $inputs.each(function() {
        values[this.name] = $(this).val();
      });
      var self = this;
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
