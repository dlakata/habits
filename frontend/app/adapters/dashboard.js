import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({
  buildURL: function(type) {
    return this.host + '/user/' + record.get('user.id') + '/habits/';
  }
});
