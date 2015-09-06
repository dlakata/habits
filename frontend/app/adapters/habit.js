import ApplicationAdapter from './application';

export default ApplicationAdapter.extend({
  buildURL: function(type, id, record) {
    var url = this.host + '/user/' + this.store.find('user') + '/habits';
    if (id !== null) {
      url += '/' + id;
    }
    return url;
  }
});
