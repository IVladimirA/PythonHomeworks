from math import log


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.known = dict()

    def fit(self, X, y, y_d):
        """ Fit Naive Bayes classifier according to X, y. """
        k_cnt = len(y_d)
        for i in range(len(y)):
            words = X[i].split()
            print(words)
            for word in words:
                if word not in self.known:
                    print(word)
                    self.known[word] = [0] * (2 * k_cnt + 1)
                print(self.known[word])
                self.known[word][y_d[y[i]]] += 1
                self.known[word][2 * k_cnt] += 1
        d = len(self.known)
        y_cnt = [0] * k_cnt
        for key in self.known.keys():
            for i in range(k_cnt):
                y_cnt[i] += self.known[key][i]
        for key in self.known.keys():
            for i in range(k_cnt):
                self.known[key][k_cnt + i] = (self.known[key][i] + self.alpha) / (
                    self.known[key][2 * k_cnt] + self.alpha * d
                )
        for key in self.known.keys():
            print(key, self.known[key])

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        pass

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        pass


x = [
    "i love this sandwich",
    "this is an amazing place",
    "i feel very good about these beers",
    "this is my best work",
    "what an awesome view",
    "i do not like this restaurant",
    "i am tired of this stuff",
    "i can't deal with this",
    "he is my sworn enemy",
    "my boss is horrible",
]
y = [
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Positive",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
    "Negative",
]
y_dict = {"Positive": 0, "Negative": 1}
test = NaiveBayesClassifier(0.1)
test.fit(x, y, y_dict)
