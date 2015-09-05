import Ember from 'ember';

export default Ember.Route.extend({
  model: function () {
    return [{
      id: 1,
      title: "Go to the gym",
      description: "Make sure to work out at the gym for at least 30 minutes a day",
      time: 30,
      goal: 60
    }, {
      id: 2,
      title: "Brush teeth",
      description: "Brush teeth twice a day or after every meal",
      time: 25,
      goal: 200
    }];
  }
});