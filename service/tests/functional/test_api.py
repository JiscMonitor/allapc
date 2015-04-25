from unittest import TestCase
from service import models
import requests, json, time
from copy import deepcopy

API = "http://localhost:5016/api/apc"
LOCAL = "http://localhost:5016/api/local"

MONITOR = {
    "dc:source": {
        "name": "Some Journal Or Other"
    },
    "license_ref": {
        "title": "CC-BY"
    },
    "rioxxterms:project": [
        {
            "grant_number": "RES-061-25-0409",
            "name": "ESRC"
        }
    ],
    "rioxxterms:type": "Journal Article/Review (Hybrid journal)",
    "@context": {
        "jm": "http://jiscmonitor.jiscinvolve.org/",
        "dcterms": "http://purl.org/dc/terms/",
        "dc": "http://purl.org/dc/elements/1.1/",
        "rioxxterms": "http://rioxx.net/v2-0-beta-1/"
    },
    "jm:apc": [
        {
            "currency": "GBP",
            "amount": 1680,
            "amount_gbp": 1680,
            "fund": [
                {
                    "name": "RCUK"
                }
            ],
            "name": "Cottage Labs"
        }
    ],
    "dcterms:publisher": {
        "name": "Me"
    }
}

class TestModels(TestCase):

    def setUp(self):
        super(TestModels, self).setUp()

    def tearDown(self):
        super(TestModels, self).tearDown()

    def test_01_create(self):
        resp = requests.post(API, json.dumps(MONITOR))
        assert resp.status_code == 201
        assert "location" in resp.headers

    def test_02_retrieve(self):
        resp = requests.post(API, json.dumps(MONITOR))
        location = resp.headers.get("location")
        resp2 = requests.get(location)
        j = resp2.json()
        assert j.get("dc:source", {}).get("name") == "Some Journal Or Other"

    def test_03_update(self):
        resp = requests.post(API, json.dumps(MONITOR))
        location = resp.headers.get("location")

        m2 = deepcopy(MONITOR)
        m2["dc:source"]["name"] = "An alternative name"
        resp2 = requests.put(location, json.dumps(m2))
        assert resp2.status_code == 200

        resp3 = requests.get(location)
        j = resp3.json()
        assert j.get("dc:source", {}).get("name") == "An alternative name"

    def test_04_delete(self):
        resp = requests.post(API, json.dumps(MONITOR))
        location = resp.headers.get("location")

        resp2 = requests.delete(location)
        assert resp2.status_code == 200

        resp3 = requests.get(location)
        assert resp3.status_code == 404

    def test_05_local_id(self):
        resp = requests.post(API, json.dumps(MONITOR), headers={"slug" : "richardsid"})
        time.sleep(2)
        resp2 = requests.get(LOCAL + "/richardsid")
        assert resp2.status_code == 200
        j = resp2.json()
        assert j.get("dc:source", {}).get("name") == "Some Journal Or Other"