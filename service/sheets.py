from octopus.lib import clcsv

class APCSheet(clcsv.SheetWrapper):
    HEADERS = {
         u'APC paid (actual currency) including VAT if charged':                    u'amount',
         u'APC paid (\xa3) including VAT if charged':                               u'amount_gbp',
         u'Additional costs (\xa3)':                                                u'additional_costs',
         u'Affiliated author':                                                      u'affiliated_author',
         u'Amount of APC charged to COAF grant (include VAT if charged) in \xa3':   u'coaf',
         u'Article title':                                                          u'title',
         u'Correct license applied?':                                               u'licence_received',
         u'Currency of APC':                                                        u'currency',
         u'DOI':                                                                    u'doi',
         u'Date of APC payment':                                                    u'apc_payment_date',
         u'Date of initial application by author':                                  u'initial_application_date',
         u'Date of publication':                                                    u'publication_date',
         u'Discounts, memberships & pre-payment agreements':                        u'discounts',
         u'Fund that APC is paid from (1)':                                         u'fund_1',
         u'Fund that APC is paid from (2)':                                         u'fund_2',
         u'Fund that APC is paid from (3)':                                         u'fund_3',
         u'Funder of research (1)':                                                 u'funder_1',
         u'Funder of research (2)':                                                 u'funder_2',
         u'Funder of research (3)':                                                 u'funder_3',
         u'Grant number (1)':                                                       u'grant_number_1',
         u'Grant number (2)':                                                       u'grant_number_2',
         u'Grant number (3)':                                                       u'grant_number_3',
         u'ISSN':                                                                   u'issn',
         u'Journal':                                                                u'source',
         u'Licence':                                                                u'licence',
         u'Notes':                                                                  u'notes',
         u'Problem-free open access publication?':                                  u'publication_process_feedback',
         u'PubMed Central (PMC) ID':                                                u'pmcid',
         u'PubMed ID':                                                              u'pmid',
         u'Publisher':                                                              u'publisher',
         u'Submitted by':                                                           u'submitted_by',
         u'Type of publication':                                                    u'type',
         u'University department':                                                  u'department'
    }

    EMPTY_STRING_AS_NONE = True

    TRIM = True