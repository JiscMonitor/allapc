from portality.modules.es import dao

class InstitutionalRecordDAO(dao.ESDAO):
    __type__ = 'institutional'

class APCRecordDAO(dao.ESDAO):
    __type__ = 'apc'