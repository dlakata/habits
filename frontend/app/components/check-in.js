import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['checkin'],
  checked: '',

  image: function() {
    var checked = this.get('checked');
    if (checked === false) {
      return '/assets/images/notok.png';
    } else if (checked === true) {
      return '/assets/images/ok.png';
    } else if (checked === 'maybe') {
      return '/assets/images/attention.png';
    } else {
      return '/assets/images/rating.png';
    }
  }.property('checked'),

  actions: {
    habitDone: function(_status) {
      console.log("You clicked " + _status + " for " + this.habit.title + "!");
      if (_status === 'yes') {
        this.set('checked', true);
      } else if (_status === 'no') {
        this.set('checked', false);
      } else if (_status === 'maybe') {
        this.set('checked', 'maybe');
      }
    }
  }
});
