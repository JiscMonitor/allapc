from octopus.modules.es import dao

class InstitutionalRecordDAO(dao.ESDAO):
    __type__ = 'institutional'

    @classmethod
    def find_by_local_id(cls, local_id, account_id):
        liq = LocalIDQuery(local_id, account_id)
        return cls.object_query(q=liq.query())

class LocalIDQuery(object):
    def __init__(self, local_id, account_id):
        self.local_id = local_id
        self.account_id = account_id

    def query(self):
        q = {
            "query" : {
                "bool" : {
                    "must" : [
                        {"term" : {"admin.local_id.exact" : self.local_id}},
                        {"term" : {"admin.account.exact" : self.account_id}}
                    ]
                }
            }
        }
        return q

class APCRecordDAO(dao.ESDAO):
    __type__ = 'apc'