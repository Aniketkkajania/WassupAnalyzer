from googletrans import Translator
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax

MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
def google_text_translate(text, dest_lang):
    translator = Translator()
    return translator.translate(text, dest = dest_lang).text


def polarity_scores_roberta(example):
  encoded_text = tokenizer(example, return_tensors = 'pt')
  output = model(**encoded_text)
  scores = output[0][0].detach().numpy()
  scores = softmax(scores)
  scores_dict = {'Negative': scores[0],
               'Neutral': scores[1],
               'Positive': scores[2]}
  return scores_dict