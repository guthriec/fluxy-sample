var app = app || {};

(function() {
  app.RegModel = Backbone.Model.extend({
    url: "/api/v1/register/"
  });
})();
