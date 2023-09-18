import requests
import random
import re

# A small experiment with Wikipedia which chooses a random search
# result from the inital word and finds a random word from that wikipedia
# page and continues doing so until the max count + 1 is reached.

WIKI_SEARCH_URL = "https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search="
WIKI_QUERY_URL = "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles="
INIT_PHRASE = "Acorn"
MAX_COUNT = 20


def main():
    count = 0
    phrase = INIT_PHRASE

    print(str(count + 1) + ": " + phrase)

    while count < MAX_COUNT:
        srchResp = requests.get(WIKI_SEARCH_URL + phrase)
        srchRespJson = srchResp.json()[1]
        randNum = random.randint(0, len(srchRespJson) - 1)
        selectedPhrase = srchRespJson[randNum]
        selectedPhrase = selectedPhrase.replace(" ", "_")
        print("Selected phrase: " + selectedPhrase)

        qryResp = requests.get(WIKI_QUERY_URL + selectedPhrase)
        qryRespJson = qryResp.json()["query"]["pages"]
        pageID = list(qryRespJson.keys())[0]
        qryContent = qryRespJson[pageID]["revisions"][0]["*"]
        nextPhraseOptions = re.findall(r'\b\w{4,}\b', qryContent)
        randNum = random.randint(0, len(nextPhraseOptions) - 1)
        phrase = nextPhraseOptions[randNum]

        count += 1
        print(str(count + 1) + ": " + phrase)


if __name__ == "__main__":
    main()
