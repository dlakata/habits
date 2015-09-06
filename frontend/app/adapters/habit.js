import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({
  buildURL: function(type, id, record) {
    return this.host + '/user/' + record.get('user.id') + '/habits/' + id;
  }
});
