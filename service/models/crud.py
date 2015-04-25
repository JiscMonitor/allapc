from octopus.modules.crud.models import ES_CRUD_Wrapper, CRUDObject
from service.models import Monitor, InstitutionalRecord

class InstitutionalRecordCrud(ES_CRUD_Wrapper):

    INNER_TYPE = InstitutionalRecord

    def __init__(self, raw=None, headers=None):
        # we're deliberately overriding the behaviour of the super class
        # super(InstutionalRecordCrud, self).__init__(raw, headers)
        if raw is not None:
            monitor = Monitor(raw)
            self.inner = self.INNER_TYPE()
            self.inner.monitor = monitor
            if headers is not None:
                local_id = headers.get("slug")
                if local_id is not None:
                    self.inner.local_id = local_id
        else:
            self.inner = self.INNER_TYPE()

    def json(self):
        return self.inner.monitor.json()

    def update(self, data, headers=None):
        monitor = Monitor(data)
        self.inner.monitor = monitor
        if headers is not None:
            local_id = headers.get("slug")
            if local_id is not None:
                self.inner.local_id = local_id

    @classmethod
    def get_by_local_id(cls, local_id):
        inners = cls.INNER_TYPE.find_by_local_id(local_id)

        # local ids might not be unique right now - until we enforce accounts
        if len(inners) == 0 or len(inners) > 1:
            return None

        this = cls()
        this.inner = inners[0]
        return this

