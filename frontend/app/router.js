import Ember from 'ember';
import config from './config/environment';

var Router = Ember.Router.extend({
  location: config.locationType
});

Router.map(function() {
  this.route('login');
  this.route('dashboard');
  this.route('habit', { path: '/habit/:habit_id' });
  this.route('new-habit');
  this.route('checkin');
});

export default Router;
