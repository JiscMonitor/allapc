import esprit

local = esprit.raw.Connection("http://localhost:9200", "allapc")
ooz = esprit.raw.Connection("http://ooz.cottagelabs.com:9200", "allapc")

esprit.tasks.copy(ooz, "institutional", local, "institutional")