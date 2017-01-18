import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import ShuffleSplit
from sklearn.linear_model import SGDClassifier

dataset = pd.read_csv('data/cleaned_data.csv').dropna()

tfidf_vectorizer = TfidfVectorizer(analyzer = "word", ngram_range=(1, 4))

X = tfidf_vectorizer.fit_transform(dataset['source'])
y = dataset['language']

clf = SGDClassifier()
cv = ShuffleSplit(len(y), n_iter=5, test_size=0.2, random_state=0)

parameters = {'loss': ('log', 'hinge'),
              'penalty': ['none', 'l1', 'l2', 'elasticnet'],
              'alpha': [0.001, 0.0001, 0.00001, 0.000001]
}

gs_clf = GridSearchCV(clf, parameters, cv=cv, n_jobs=-1)
gs_clf.fit(X, y)

print('Best parameters:', gs_clf.best_params_)
print('Best score:', gs_clf.best_score_)