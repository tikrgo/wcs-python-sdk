from wcs.services.mgrbase import MgrBase
from wcs.commons.http import _post
from wcs.commons.http import _get
from wcs.commons.util import urlsafe_base64_encode,https_check

from wcs.commons.logme import debug, error

class Fmgr(MgrBase):

    def __init__(self, auth,url):
        super(Fmgr, self).__init__(auth,url)

    def _generate_data_dict(self, fops,notifyurl=None, separate=None):
        data = {'fops': fops}
        if notifyurl:
            data['notifyURL'] = urlsafe_base64_encode(notifyurl)
        if separate:
            data['separate'] = separate
        return data

    def _fmgr_commons(self, method, fops,notifyurl=None,separate=None):
        url = '{0}/fmgr/{1}'.format(self.mgr_host,method)
        data = self._generate_data_dict(fops,notifyurl,separate)
        reqdata = super(Fmgr, self)._params_parse(data)
        debug('Fmgr_%s request body is: %s' % (method,reqdata))
        debug('Start to %s file' % method)
        code, text = _post(url=url, data=reqdata, headers=super(Fmgr, self)._gernerate_headers(url, body=reqdata)) 
        debug('The return code : %d ,text : %s' % (code, text))
        return code, text

    def fmgr_move(self, fops,notifyurl=None,separate=None):
        return self._fmgr_commons('move',fops,notifyurl=None,separate=None)

    def fmgr_copy(self, fops, notifyurl=None, separate=None):
        return self._fmgr_commons('copy',fops, notifyurl=None, separate=None)
   
    def fmgr_fetch(self, fops, notifyurl=None, force=None, separate=None):
        return self._fmgr_commons('fetch',fops, notifyurl=None, separate=None) 

    def fmgr_delete(self, fops, notifyurl=None, separate=None):
        return self._fmgr_commons('delete',fops, notifyurl=None, separate=None)

    def prefix_delete(self, reqdata):
        url = '{0}/fmgr/{1}'.format(self.mgr_host,'deletePrefix')
        url = https_check(url)
        debug('Fmgr_%s request body is: %s' % ('deletePrefix',reqdata))
        debug('Start to %s file' % 'deletePrefix')
        return _post(url=url, data=reqdata, headers=super(Fmgr, self)._gernerate_headers(url, body=reqdata)) 

    def m3u8_delete(self, fops, notifyurl=None, separate=None):
        return self._fmgr_commons('deletem3u8',fops, notifyurl=None, separate=None)
   
    def status(self, persistentId):
        url = '{0}/fmgr/status?persistentId={1}'.format(self.mgr_host, persistentId)
        debug('Start to get status of persistentId: %s' % persistentId)
        code, text = _get(url=url)
        debug('The return code : %d, text : %s' % (code, text))
        return code, text
