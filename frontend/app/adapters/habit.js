import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({
  buildURL: function(type, id) {
    var url = this.host + '/user/' + this.store.findAll('user') + '/habits';
    if (id !== null) {
      url += '/' + id;
    }
    return url;
  }
});
