import Ember from 'ember';

export default Ember.Component.extend({
  classNames: ['checkin'],
  checked: '',

  image: function() {
    var checked = this.get('checked');
    if (checked === false) {
      return 'notok.png';
    } else if (checked === true) {
      return 'ok.png';
    } else if (checked === 'maybe') {
      return 'attention.png';
    } else {
      return 'rating.png';
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
