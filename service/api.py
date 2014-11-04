from service import models

class RetrieveException(Exception):
    pass

class NoSuchRecordException(Exception):
    pass

class APC_API(object):

    @classmethod
    def create(self, data, local_id=None, account=None, **kwargs):
        monitor = models.Monitor(data)
        ir = models.InstitutionalRecord()
        ir.monitor = monitor
        if local_id is not None:
            ir.local_id = local_id
        if account is not None:
            ir.account_id = account.id
        ir.save()
        return ir

    @classmethod
    def retrieve(cls, apc_id):
        return models.InstitutionalRecord.pull(apc_id)

    @classmethod
    def retrieve_by_local_id(cls, local_id, account, **kwargs):
        res = models.InstitutionalRecord.find_by_local_id(local_id, account.id)
        if len(res) == 0:
            return None
        if len(res) == 1:
            return res[0]
        if len(res) > 1:
            raise RetrieveException("More than one record with that local_id for that account")
        return None

    @classmethod
    def replace(cls, apc_id, data, account=None, local_id=None, **kwargs):
        ir = models.InstitutionalRecord.pull(apc_id)
        if ir is None:
            raise NoSuchRecordException("Could not locate a record with id " + str(apc_id))

        monitor = models.Monitor(data)
        ir.monitor = monitor
        if local_id is not None:
            ir.local_id = local_id
        if account is not None:
            ir.account_id = account.id
        ir.save()

        return ir

    @classmethod
    def delete(cls, apc_id, **kwargs):
        ir = models.InstitutionalRecord.pull(apc_id)
        if ir is None:
            raise NoSuchRecordException("Could not locate a record with id " + str(apc_id))
        ir.delete()

class APIAuthoriseException(Exception):
    pass

class AuthNZ_APC_API(APC_API):

    @classmethod
    def create(cls, data, local_id=None, account=None, **kwargs):
        if account is None:
            raise APIAuthoriseException("Account must be provided to create an object")

        # FIXME: here is where we implement access controls

        return APC_API.create(data, local_id=local_id, account=account, **kwargs)

    @classmethod
    def retrieve(cls, apc_id):
        return APC_API.retrieve(apc_id)

    @classmethod
    def retrieve_by_local_id(cls, local_id, account, **kwargs):
        # FIXME: here is where we implement access controls

        return APC_API.retrieve_by_local_id(local_id, account, **kwargs)

    @classmethod
    def replace(cls, apc_id, data, account=None, local_id=None, **kwargs):
        if account is None:
            raise APIAuthoriseException("Account must be provided to replace an object")

        # FIXME: here is where we implement access controls (e.g. check the record belongs to the user in the first plage)

        return APC_API.replace(apc_id, data, local_id=local_id, account=account, **kwargs)

    @classmethod
    def delete(cls, apc_id, account=None, **kwargs):
        if account is None:
            raise APIAuthoriseException("Account must be provided to replace an object")

        # FIXME: here is where we implement access controls (e.g. check the record belongs to the user in the first plage)

        return APC_API.delete(apc_id, **kwargs)