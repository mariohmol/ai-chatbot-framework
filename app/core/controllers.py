import html2text

from flask import Blueprint, request

from app.commons import buildResponse
from app.core.intentClassifier import IntentClassifier
import app.core.sequenceLabeler as sequenceLabeler
import app.core.nlp as nlp

core = Blueprint('core_blueprint', __name__, url_prefix='/core')


@core.route('/buildModel/<storyId>', methods=['POST'])
def buildModel(storyId):
    sequenceLabeler.train(storyId)
    intentClassifier = IntentClassifier()
    botId='default'
    if request.args.get('botId'):
        botId=request.args.get('botId')
    intentClassifier.setBotId(botId)
    intentClassifier.train()
    return buildResponse.sentOk()


@core.route('/sentenceTokenize', methods=['POST'])
def sentenceTokenize():
    sentences = html2text.html2text(request.form['sentences'])
    result = nlp.sentenceTokenize(sentences)
    return buildResponse.sentPlainText(result)


@core.route('/posTagAndLabel', methods=['POST'])
def posTagAndLabel():
    content = request.get_json(silent=True)
    sentences = None
    if content:
        sentences = content.get("sentences")
    if not sentences:
        sentences = request.form['sentences']
    cleanSentences = html2text.html2text(sentences)
    result = nlp.posTagAndLabel(cleanSentences)
    return buildResponse.buildJson(result)