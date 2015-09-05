import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('task-details', { path: '/task/:task_id' });
  this.route('checkin');
});

export default Router;
