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
   * @desc: Utility function to convert a Javascript date object into a string
   *        suitable for presenting to a restaurant end-user.
   * @param: date - a Javascript date object
   * @returns: string formatted, e.g., Sunday April 27 2:30 PM
   */
  FluxyTime.getDateString = function(date) {
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
    return dayOfWeek + " " + month + " " + day + " - " + hours +
             ":" + minutes + " " + amPm;
  };
  
  return FluxyTime;
});
