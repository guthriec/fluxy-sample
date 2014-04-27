/*
 * @author: Ayush
 * @desc: Defines the view that is associated with the form that allows vendors
 * to create a new deal. It is responsible for handling all events associated
 * with the form.
 */
define([
  'marionette',
  'vent'
], function(Marionette, vent) {
  var DealCreateFormView = Marionette.ItemView.extend({
    events: {
      'click #submit-btn': 'createDeal'
    },
    template: '#deal-create-form-template',

    render: function() {
      this.$el.html(_.template($(this.template).html()));

      var currDate = new Date();
      var currDay = currDate.getDate();
      var latestDate = new Date();
      latestDate.setDate(currDay + 7);
      var monthNames = [ "January", "February", "March", "April", "May", "June",
                         "July", "August", "September", "October", "November",
                         "December" ]
      var dayNames = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                       "Friday", "Saturday" ]
      var daySelect = this.$el.find('#start-day');
      daySelect.empty();
      var possibleDay = new Date();
      possibleDay.setHours(0);
      possibleDay.setMinutes(0);
      possibleDay.setSeconds(0);
      possibleDay.setMilliseconds(0);
      for (var i=0; i < 8; i++) {
        possibleDay.setDate(currDay + i);
        daySelect.append('<option value="' + possibleDay.getTime()  + '">' + 
                         dayNames[possibleDay.getDay()] + ', ' + 
                         monthNames[possibleDay.getMonth()] + ' ' + 
                         possibleDay.getDate().toString() + '</option>');
      }

      this.$el.find('input:radio[name="limit"]').change(
        function() {
          if($(this).is(':checked') && (this).value == 'limited') {
            $('#max-deals-number').prop('disabled', false);
            $('#max-deals-number').attr('placeholder', '1  --  500');
            $('#max-deals-number').attr('maxlength', '3');
          }
          if($(this).is(':checked') && (this).value == 'unlimited') {
            $('#max-deals-number').prop('disabled', true);
            $('#max-deals-number').attr('placeholder', 'Unlimited');
            $('#max-deals-number').val('');
          }
        }
      );
      return this;
    },

    createDeal: function(e) {
      e.preventDefault();

      var newModel = {};

      var $formInputs = $('#deal-form :input');
      var formValues = {};
      $formInputs.each(function() {
        formValues[this.name] = this.value;
      });
      newModel['title'] = formValues['title'];
      newModel['desc'] = formValues['desc'];
      var timeStart = new Date();
      var startHours = Number(formValues['start-hours']);
      if(formValues['start-am-pm'] == 'pm') {
        startHours += 12;
      } else if(startHours == 12) {
        startHours = 0;
      }
      var startMinutes = Number(formValues['start-minutes']) + 60 * startHours;
      timeStart.setTime(Number(formValues['start-day']) + 60000 * startMinutes);
      newModel['time_start'] = timeStart;
      var minutes = Number(formValues['duration-minutes']) + 
                    60 * Number(formValues['duration-hours']);
      var timeEnd = new Date();
      timeEnd.setTime(timeStart.getTime() + minutes * 60000);
      newModel['time_end'] = timeEnd;
      newModel['max_deals'] = -1;
      var limitRadio = this.$el.find('input:radio[value="limited"]');
      if(limitRadio.is(':checked')) {
        newModel['max_deals'] = Number(formValues['max-deals']);
      }
      newModel['instructions'] = 'Show to waiter';
      console.log('createDealConfirmTrigger sent');
      vent.trigger('createDealConfirmTrigger', newModel);
      this.$el.find('#submit-btn').blur();
    }
  });
  return DealCreateFormView;
});
