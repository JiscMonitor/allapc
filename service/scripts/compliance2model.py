from service import models
from octopus.lib import clcsv
import json, codecs

class ComplianceSheet(clcsv.SheetWrapper):
    HEADERS = {
        "PMCID" : "pmcid",
        "PMID" : "pmid",
        "DOI" : "doi",
        "Article title" : "title",
        "ISSN" : "split_issn",
        "Publisher" : "publisher",
        "Metadata in CORE?" : "core",
        "Fulltext in EPMC?" : "epmc",
        "XML Fulltext in EPMC?" : "epmc_xml",
        "AAM in EPMC?" : "epmc_aam",
        "Licence" : "license_title",
        "Journal Type" : "custom_oa_type",
        "Self-Archive Preprint" : "sapr_policy",
        "Preprint Embargo" : "sapr_embargo",
        "Self-Archive Postprint" : "sapo_policy",
        "Postprint Embargo" : "sapo_embargo",
        "Self-Archive Publisher Version" : "sapu_policy",
        "Publisher Version Embargo" : "sapu_embargo"
    }

    EMPTY_STRING_AS_NONE = True


class ComplianceMonitor(models.Monitor):

    def __init__(self, raw=None):
        super(ComplianceMonitor, self).__init__(raw)
        self.epmc_repo = models.Repository()
        self.in_epmc = False

    @property
    def split_issn(self):
        return None

    @split_issn.setter
    def split_issn(self, val):
        if val is None:
            return
        bits = val.split(",")
        for b in bits:
            self.add_issn(b.strip())

    @property
    def custom_oa_type(self):
        return None

    @custom_oa_type.setter
    def custom_oa_type(self, val):
        if val == "unknown":
            return
        self.oa_type = val

    @property
    def core(self):
        return None

    @core.setter
    def core(self, val):
        if val == "True":
            r = models.Repository()
            r.name = "CORE"
            r.url = "http://core.ac.uk/"
            self.add_repository(r)

    @property
    def epmc(self):
        for r in self.repository:
            if r.name == "EPMC":
                return r
        return self.epmc_repo

    @epmc.setter
    def epmc(self, val):
        if val == "True":
            self.epmc_repo.name = "EPMC"
            self.epmc_repo.url = "http://europepmc.org/"
            self.add_repository(self.epmc_repo)

    @property
    def epmc_xml(self):
        return None

    @epmc_xml.setter
    def epmc_xml(self, val):
        val = True if val == "True" else False
        self.epmc.machine_readable_fulltext = val

    @property
    def epmc_aam(self):
        return None

    @epmc_aam.setter
    def epmc_aam(self, val):
        val = True if val == "True" else False
        self.epmc.aam = val

    @property
    def license_title(self):
        return None

    @license_title.setter
    def license_title(self, val):
        if val is None or val == "unknown": return
        self.set_license(val)

    @property
    def sapr_policy(self):
        return None

    @sapr_policy.setter
    def sapr_policy(self, val):
        if val is None: return
        self._set_single("dc:source.self_archiving.preprint.policy", val, coerce=self._utf8_unicode())

    @property
    def sapr_embargo(self):
        return None

    @sapr_embargo.setter
    def sapr_embargo(self, val):
        if val is None: return
        val = val.split(" ")[0]
        self._set_single("dc:source.self_archiving.preprint.embargo", val, coerce=self._int())

    @property
    def sapo_policy(self):
        return None

    @sapo_policy.setter
    def sapo_policy(self, val):
        if val is None: return
        self._set_single("dc:source.self_archiving.postprint.policy", val, coerce=self._utf8_unicode())

    @property
    def sapo_embargo(self):
        return None

    @sapo_embargo.setter
    def sapo_embargo(self, val):
        if val is None: return
        val = val.split(" ")[0]
        self._set_single("dc:source.self_archiving.postprint.embargo", val, coerce=self._int())

    @property
    def sapu_policy(self):
        return None

    @sapu_policy.setter
    def sapu_policy(self, val):
        if val is None: return
        self._set_single("dc:source.self_archiving.publisher.policy", val, coerce=self._utf8_unicode())

    @property
    def sapu_embargo(self):
        return None

    @sapu_embargo.setter
    def sapu_embargo(self, val):
        if val is None: return
        val = val.split(" ")[0]
        self._set_single("dc:source.self_archiving.publisher.embargo", val, coerce=self._int())

def convert(file_path):
    sheet = ComplianceSheet(file_path)
    obs = [o.data for o in sheet.dataobjs(ComplianceMonitor)]
    return obs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument("-i",
                        "--input",
                        help="Input file to convert to model objects")

    parser.add_argument("-o",
                        "--out",
                        help="Output file to dump the results")

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        exit()

    obs = convert(args.input)
    res = json.dumps(obs, indent=2)

    if args.out:
        with codecs.open(args.out, "wb") as f:
            f.write(res)
    else:
        print res





