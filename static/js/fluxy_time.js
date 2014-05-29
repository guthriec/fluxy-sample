/*
 * @author: Chris
 * @desc: Defines a FluxyTime module to handle date string readability
 *        and API time standards.
 */
define([
], function() {
  FluxyTime = {};
  FluxyTime.monthNames = [ "January", "February", "March", "April", "May",
                           "June", "July", "August", "September", "October",
                           "November", "December" ];
  FluxyTime.dayNames = [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
                         "Friday", "Saturday" ];
  
  /*
   * @author: Chris
   * @desc: Takes a Javascript date object and returns a new date object
   *        with the same hours and minutes, but on the current date
   * @param: date - a Javascript date object
   * @returns: date with same time on current date
   */
  FluxyTime.sameTimeToday = function(date) {
      var oldHours = date.getHours();
      var oldMinutes = date.getMinutes();
      var newDate = new Date();
      newDate.setMilliseconds(0);
      newDate.setSeconds(0);
      newDate.setMinutes(oldMinutes);
      newDate.setHours(oldHours);
      return newDate;
  };

  /*
   * @author: Chris
   * @desc: Utility function to convert a Javascript date object into a string
   *        suitable for presenting to a restaurant end-user.
   * @param: date - a Javascript date object
   * @returns: string formatted, e.g., Sunday April 27 2:30 PM
   */
  FluxyTime.getDateStringHTML = function(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    if (minutes < 10) {
      minutes = "0" + minutes;
    }
    var amPm = "AM";
    if (hours > 12) {
      amPm = "PM";
      hours -= 12;
    }
    var month = FluxyTime.monthNames[date.getMonth()];
    var day = date.getDate();
    var dayOfWeek = FluxyTime.dayNames[date.getDay()];
    return dayOfWeek + " " + month + " " + day + "<br>" + hours +
             ":" + minutes + " " + amPm;
  };
  
  return FluxyTime;
});
