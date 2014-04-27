define([
  'jquery'
], function($) {
  var Csrf = {};
  Csrf.start = function() {
    function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    var csrfToken = "{{ csrf_token }}";
    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
          xhr.setRequestHeader("X-CSRFToken", csrfToken);
        }
      }
    });
  }
  return Csrf;
});
