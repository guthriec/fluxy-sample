/*
 * @author: Ayush
 * @desc: Defines the view that is associated with the form that allows vendors
 * to create a new deal. It is responsible for handling all events associated
 * with the form.
 */
define([
  'fluxy_time',
  'marionette',
  'vent',
  'models/deal_model',
], function(FluxyTime, Marionette, vent, DealModel) {
  var DealCreateFormView = Marionette.ItemView.extend({
    cache: { },
    template: '#deal-create-form-template',

    events: {
      'focusout #title-group' : 'validateTitleGroup',
      'focusout #subtitle-group' : 'validateSubtitleGroup',
      'focusout #duration-group' : 'validateStartAndDuration',
      'focusout #start-time-group' : 'validateStart',
      'focusout #max-deals-group' : 'validateMaxDeals',
      'change input:radio[name="limit"]' : 'changeMaxDealsState',
      'click #change-photo-btn': 'changePhoto',
      'click #submit-btn' : 'createDeal',
      // Model-Field bindings
      'change #deal-title' : 'updateModel',
      'change #deal-subtitle' : 'updateModel',
      'change #deal-desc' : 'updateModel',
      'focusout #start-time-group' : 'updateModel',
      'focusout #duration-group' : 'updateModel',
      'change #max-deals-number' : 'updateModel',
    },

    initialize: function() {
      vent.on('photoChangedTrigger', this.photoChanged, this);
    },

    updateModel: function(e) {
      superduper = this.deal;
      var changed = e.currentTarget;

      var obj = { };
      if (changed.id == 'max-deals-number') {
        obj['max_deals'] = this.getMaxDeals();
      } else if (changed.id == 'start-time-group') {
        obj['time_start'] = this.computeStart().toISOString();
        // Cache elem values
        this.cache['start-day'] = this.$el.find('#start-day').val();
        this.cache['start-hours'] = this.$el.find('#start-hours').val();
        this.cache['start-minutes'] = this.$el.find('#start-minutes').val();
        this.cache['start-am-pm'] = this.$el.find('#start-am-pm').val();
      } else if (changed.id == 'duration-group') {
        obj['time_end'] = this.computeEnd().toISOString();
        // Cache elem values
        this.cache['duration-hours'] = this.$el.find('#duration-hours').val();
        this.cache['duration-minutes'] = this.$el.find('#duration-minutes').val();
      } else {
        obj[changed.id.split('-')[1]] = $(changed).val();
      }

      if (this.deal)
        this.deal.set(obj);
      else
        this.deal = new DealModel(obj);
    },

    /*
     * @author: Chris
     * @desc: Utility function to take the start-day-group and start-time-group
     *         elements, extract input, and compute the start time as a
     *         Javascript date.
     */
    computeStart: function() {
      var startDayEl = this.$el.find('#start-day-group');
      var startTimeEl = this.$el.find('#start-time-group');
      var dayInputEl = startDayEl.find('select[name="start-day"]');
      var hoursInputEl = startTimeEl.find('select[name="start-hours"]');
      var minutesInputEl = startTimeEl.find('select[name="start-minutes"]');
      var amPmInputEl = startTimeEl.find('select[name="start-am-pm"]');
      var timeStart = new Date();
      var startHours = Number(hoursInputEl.val());
      if (amPmInputEl.val() == 'pm') {
        startHours += 12;
      } else if (startHours == 12) {
        startHours = 0;
      }
      var startMinutes = Number(minutesInputEl.val()) + 60 * startHours;
      timeStart.setTime(Number(dayInputEl.val()) + 60000 * startMinutes);
      return timeStart;
    },

    /*
     * @author: Chris
     * @desc: Utility function to take the duration-group element, extract
     *        input, and compute the duration.
     */
    computeDuration: function() {
      var durationEl = this.$el.find('#duration-group');
      var minutesEl = durationEl.find('#duration-minutes');
      var hoursEl = durationEl.find('#duration-hours');
      return Number(minutesEl.val()) + 60 * Number(hoursEl.val());
    },

    computeEnd: function(timeStart, minutes) {
      if (typeof(timeStart) === 'undefined')
        timeStart = this.computeStart();
      if (typeof(minutes) === 'undefined')
        minutes = this.computeDuration();
      return timeStart.getTime() + minutes * 60000;
    },

    /*
     * @author: Chris
     * @desc: Event handler to extract the input for start time,
     *        validate that the start time is after the current time, and update
     *        the form with appropriate errors.
     */
    validateStart: function(e) {
      var valid = true;
      var timeArea = this.$el.find('#time-area');
      var startTimeEl = timeArea.find('#start-time-group');
      var startGroups = timeArea.find('#start-day-group').add('#start-time-group');
      var startTime = this.computeStart();
      if (0 < (startTime - Date.now())) {
        startGroups.removeClass('has-error');
        this.$el.find('#start-validation-error').remove();
      } else {
        startGroups.addClass('has-error');

        if (this.$el.find('#start-validation-error').length == 0) {
          startTimeEl.append('<p id="start-validation-error" ' +
                             'class="help-block col-sm-offset-2 col-sm-6">' +
                             'Start time must be in the future!</p>');
        valid = false;
        }
      }
      // Attach event handlers to validate on any change, giving user immediate
      // feedback while editing the form
      this.events['change #start-day-group'] = 'validateStart';
      this.events['change #start-time-group'] = 'validateStart';
      delete this.events['focusout #start-am-pm'];
      // Register changes made to events
      this.delegateEvents();
      return valid;
    },

    /*
     * @author: Chris
     * @desc: Event handler to extract the input for deal title,
     *        validate that the title is long enough, and update
     *        the form with appropriate errors.
     */
    validateTitleGroup: function(e) {
      var valid = true;
      var titleEl = this.$el.find('#title-group');
      var titleInputEl = titleEl.find('input:text[name="deal-title"]');
      var title = titleInputEl.val();
      if (title.length > 7 && title.length < 16) {
        titleEl.removeClass('has-error');
        this.$el.find('#title-validation-error').remove();
      } else {
        titleEl.addClass('has-error');
        var errorEl = this.$el.find('#title-validation-error');
        if (errorEl.length == 0) {
          this.$el.find('#deal-title-container').after(
                                             '<p id="title-validation-error" ' +
                                             'class="help-block col-sm-offset-2' +
                                             ' col-sm-6">Deal title must be ' +
                                             'between 8 and 15 characters in length.</p>');
        }
        valid = false;
      }
      // Attach event handlers to validate on any change, giving user immediate
      // feedback while editing the form
      this.events['keyup #title-group'] = 'validateTitleGroup';
      delete this.events['focusout #title-group'];
      // Register changes made to events
      this.delegateEvents();
      return valid;
    },

    validateSubtitleGroup: function(e) {
      var valid = true;
      var subtitleEl = this.$el.find('#subtitle-group');
      var subtitleInputEl = subtitleEl.find('input:text[name="deal-subtitle"]');
      var subtitle = subtitleInputEl.val();
      if (subtitle.length < 41) {
        subtitleEl.removeClass('has-error');
        this.$el.find('#subtitle-validation-error').remove();
      } else {
        subtitleEl.addClass('has-error');
        var errorEl = this.$el.find('#subtitle-validation-error');
        if (errorEl.length == 0) {
          this.$el.find('#deal-subtitle-container').after(
                                             '<p id="subtitle-validation-error" ' +
                                             'class="help-block col-sm-offset-2' +
                                             ' col-sm-6">Subtitle must be less ' +
                                             'than 40 characters in length.</p>');
        }
        valid = false;
      }
      // Attach event handlers to validate on any change, giving user immediate
      // feedback while editing the form
      this.events['keyup #subtitle-group'] = 'validateSubtitleGroup';
      delete this.events['focusout #subtitle-group'];
      // Register changes made to events
      this.delegateEvents();
      return valid;
    },

    /*
     * @author: Chris
     * @desc: Event handler to extract the input for duration,
     *        validate that duration is positive, and update
     *        the form with appropriate errors.
     */
    validateDuration: function(e) {
      var valid = true;
      var durationEl = this.$el.find('#duration-group');
      var duration = this.computeDuration();

      if (duration > 0) {
        durationEl.removeClass('has-error');
        durationEl.find('#duration-validation-error').remove();
      } else {
        durationEl.addClass('has-error');
        var pEl= durationEl.find('p');
        if (!(pEl.attr('id') == 'duration-validation-error')) {
          pEl.before('<p id="duration-validation-error" ' +
                         'class="help-block col-sm-offset-2 col-sm-6">' +
                         'Duration must be greater than 0</p>');
        }
        valid = false;
      }
      // Attach event handlers to validate on any change, giving user immediate
      // feedback while editing the form
      this.events['change #duration-group'] = 'validateDuration';
      delete this.events['focusout #duration-group'];
      // Register changes made to events
      this.delegateEvents();
      return valid;
    },

    /*
     * @author: Chris
     * @desc: an event handler to validate both start and duration.
     */
    validateStartAndDuration: function(e) {
      this.validateStart(e);
      this.validateDuration(e);
    },

    /*
     * @author: Chris
     * @desc: Event handler to extract the input for maximum number of deals,
     *        validate that this is a number between 1 and 500, and update
     *        the form with appropriate errors.
     */
    validateMaxDeals: function(e) {
      var valid = true;
      var maxDealsEl = this.$el.find('#max-deals-group');
      var maxDeals = parseInt(maxDealsEl.find('#max-deals-number').val(), 10);
      var maxDealsRadio = this.$el.find('#max-deals-radio');
      var radioSelection = this.$el.find('#max-deals-radio ' +
                                         'input[type=radio]:checked');
      if (radioSelection.length == 0) {
        maxDealsRadio.addClass('has-error');
        if (this.$el.find('#max-deals-radio-validation-error').length == 0) {
          maxDealsRadio.append('<p id="max-deals-radio-validation-error" ' +
                               'class="help-block col-sm-6">' +
                               'Select an option!</p>');
        }
        valid = false;
      } else {
        maxDealsRadio.removeClass('has-error');
        maxDealsRadio.find('#max-deals-radio-validation-error').remove();
      }

      if (this.$el.find('#unlimited').checked ||
          (!isNaN(maxDeals) && maxDeals > 0 && maxDeals <= 500)) {
        maxDealsEl.removeClass('has-error');
        maxDealsEl.find('#max-deals-validation-error').remove();
      } else {
        maxDealsEl.addClass('has-error');
        if (this.$el.find('#max-deals-validation-error').length == 0) {
          maxDealsEl.append('<p id="max-deals-validation-error" ' +
                            'class="help-block col-sm-6">' +
                            'Maximum number of deals must be a number between' +
                            ' 1 and 500 (inclusive)</p>');
        }
        valid = false;
      }
      // Attach event handlers to validate on any change, giving user immediate
      // feedback while editing the form
      this.events['keyup #max-deals-group'] = 'validateMaxDeals';
      this.events['click #max-deals-radio'] = 'validateMaxDeals';
      delete this.events['focusout #max-deals-group'];
      // Register changes made to events
      this.delegateEvents();
      return valid;
    },

    validatePhoto: function(e) {
      photoEl = this.$el.find('#photo-group');
      photoContainer = this.$el.find('#photo-container');
      if (this.photo) {
        photoEl.removeClass('has-error');
        this.$el.find('#photo-validation-error').remove();
        return true;
      } else {
        var errorEl = this.$el.find('#photo-validation-error');
        if (errorEl.length == 0) {
          photoEl.addClass('has-error');
          photoContainer.after('<p id="photo-validation-error" ' +
                               'class="help-block col-sm-6 col-sm-offset-2">' +
                               'Must choose a deal photo</p>');
        }
        return false;
      }
    },

    validateAll: function(e) {
      var startValid = this.validateStart(e);
      var titleValid = this.validateTitleGroup(e);
      var subtitleValid = this.validateSubtitleGroup(e);
      var durationValid = this.validateDuration(e);
      var maxDealsValid = this.validateMaxDeals(e);
      var photoValid = this.validatePhoto(e);
      return (startValid && titleValid && subtitleValid && durationValid
          && maxDealsValid && photoValid);
    },

    populateFromModel: function() {
      if (this.deal) {
        this.$el.find('#deal-title').val(this.deal.get('title'));
        this.$el.find('#deal-subtitle').val(this.deal.get('subtitle'));
        this.$el.find('#deal-desc').val(this.deal.get('desc'));
        if (this.photo)
          vent.trigger('photoChangedTrigger', this.photo);
        /* Restore start time and duration values from cache */
        if (this.cache['start-day']) {
          this.$el.find('#start-day').val(this.cache['start-day']);
          this.$el.find('#start-hours').val(this.cache['start-hours']);
          this.$el.find('#start-minutes').val(this.cache['start-minutes']);
          this.$el.find('#start-am-pm').val(this.cache['start-am-pm']);
        }
        if (this.cache['duration-hours']) {
          this.$el.find('#duration-hours').val(this.cache['duration-hours']);
          this.$el.find('#duration-minutes').val(this.cache['duration-minutes']);
        }
        /* End */
        var maxDeals = this.deal.get('max_deals');
        if (maxDeals === -1) {
          this.$el.find('input:radio[value="unlimited"]').prop('checked', true);
        } else if (maxDeals !== undefined) {
          this.$el.find('input:radio[value="limited"]').prop('checked', true);
          this.changeMaxDealsState();
          this.$el.find('#max-deals-number').val(maxDeals);
        }
        this.validateAll();
      }
    },

    render: function() {
      this.$el.html(_.template($(this.template).html()));
      var currDate = new Date();
      var currDay = currDate.getDate();
      var latestDate = new Date();
      latestDate.setDate(currDay + 7);
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
                         FluxyTime.dayNames[possibleDay.getDay()] + ', ' +
                         FluxyTime.monthNames[possibleDay.getMonth()] + ' ' +
                         possibleDay.getDate().toString() + '</option>');
      }
      // This seems to be required to cause the events hash to get
      // used when the view is rendered for a second time (i.e. after
      // another tab gets clicked on)
      this.delegateEvents();
      this.populateFromModel();
      return this;
    },

    changeMaxDealsState: function(e) {
      if (this.$el.find('#limited').is(':checked')) {
        $('#max-deals-number').prop('disabled', false);
        $('#max-deals-number').attr('placeholder', '100');
        $('#max-deals-number').attr('maxlength', '3');
      }
      else if (this.$el.find('#unlimited').is(':checked')) {
        $('#max-deals-number').prop('disabled', true);
        $('#max-deals-number').attr('placeholder', 'Unlimited');
        $('#max-deals-number').val('');
      }
    },

    /*
     * @author: Rahul
     * @desc: Triggers an event on the dashboard that shows the photo picker
     * modal.
     */
    changePhoto: function(e) {
      e.preventDefault();
      vent.trigger('changePhotoTrigger', { });
    },

    /*
     * @author: Rahul
     * @desc: Change displayed photo.
     */
    photoChanged: function(photo) {
      this.photo = photo;
      this.deal.set('photo', photo);
      this.$el.find('#deal-photo').attr('src', this.photo.get('photo'));
      this.$el.find('#deal-photo').css('display', 'block');
    },

    getMaxDeals: function() {
      var maxDeals = -1;
      var limitRadio = this.$el.find('input:radio[value="limited"]');
      if (limitRadio.is(':checked'))
        maxDeals = Number(this.$el.find('#max-deals-number').val());
      return maxDeals;
    },

    createDeal: function(e) {
      e.preventDefault();
      var buttonGroup = this.$el.find('#button-group');
      if (!this.validateAll(e)) {
        buttonGroup.addClass('has-error');
        if (this.$el.find('#submit-failure').length == 0) {
          buttonGroup.prepend('<p class="help-block col-sm-offset-2 col-sm-6" ' +
                              'id="submit-failure">Deal form not completed! ' +
                              'Go back over the form and submit again.</p>');
          window.scrollTo(0, document.body.scrollHeight);
          this.events['click #deal-form'] = function(e) {
            if (e.target.id == "submit-btn") return;
            this.$el.find('#submit-failure').remove();
          };
          this.delegateEvents();
        }
        return;
      } else {
        this.$el.find('#submit-failure').remove();
        buttonGroup.removeClass('has-error');
      }
      var newModel = {};

      var $formInputs = $('#deal-form :input');
      var formValues = {};
      $formInputs.each(function() {
        formValues[this.name] = this.value;
      });
      newModel['title'] = formValues['deal-title'];
      newModel['subtitle'] = formValues['deal-subtitle'];
      newModel['desc'] = formValues['desc'];
      var timeEnd = new Date();
      var timeStart = this.computeStart();
      newModel['time_start'] = timeStart.toISOString();
      newModel['time_end'] = this.computeEnd(timeStart).toISOString();

      newModel['max_deals'] = this.getMaxDeals();
      newModel['instructions'] = 'Show to waiter';

      newModel['photo'] = this.photo;

      vent.trigger('createDealConfirmTrigger', newModel);
      this.$el.find('#submit-btn').blur();
    }
  });
  return DealCreateFormView;
});
