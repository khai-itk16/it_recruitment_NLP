from flask import Flask, jsonify, request
import ultis
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


@app.route('/data', methods=['POST'])
def main():
    data = request.json
    text_train = ultis.markdown_to_text(data['jobRequire'])
    vectorizer = TfidfVectorizer()
    vec_train = vectorizer.fit_transform([text_train])
    for index in range(len(data['candidateFilters'])):
        text_test = ultis.markdown_to_text(data['candidateFilters'][index]['skillAndExperience'])
        vec_test = vectorizer.transform([text_test])
        cosine_similarities = cosine_similarity(vec_train, vec_test)
        data['candidateFilters'][index]['matchPercent'] = round(cosine_similarities[0][0], 2) * 100
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)