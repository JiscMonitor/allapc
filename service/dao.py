from octopus.modules.es import dao

class InstitutionalRecordDAO(dao.ESDAO):
    __type__ = 'institutional'

    @classmethod
    def find_by_local_id(cls, local_id, account_id=None):
        liq = LocalIDQuery(local_id, account_id)
        return cls.object_query(q=liq.query())

    @classmethod
    def date_statistics(cls):
        q = DateQuery()
        resp = cls.query(q=q.query())

        stats = {}
        stats["applied"] = resp.get("facets", {}).get("applied", {}).get("min")
        stats["published"] = resp.get("facets", {}).get("published", {}).get("min")
        stats["paid"] = resp.get("facets", {}).get("paid", {}).get("min")

        return stats

class DateQuery(object):
    def __init__(self):
        pass

    def query(self):
        q = {
            "query" : {"match_all" : {}},
            "size" : 0,
            "facets" : {
                "applied" : {
                    "statistical" : {
                        "field" : "jm:dateApplied"
                    }
                },
                "published" : {
                    "statistical" : {
                        "field" : "rioxxterms:publication_date"
                    }
                },
                "paid" : {
                    "statistical" : {
                        "field" : "monitor.jm:apc.date_paid"
                    }
                }
            }
        }
        return q

class LocalIDQuery(object):
    def __init__(self, local_id, account_id=None):  # FIXME: until we implement security, account_id is meaningless
        self.local_id = local_id
        self.account_id = account_id

    def query(self):
        q = {
            "query" : {
                "bool" : {
                    "must" : [
                        {"term" : {"admin.local_id.exact" : self.local_id}} #,
                        #{"term" : {"admin.account.exact" : self.account_id}}
                    ]
                }
            }
        }
        return q

class APCRecordDAO(dao.ESDAO):
    __type__ = 'apc'