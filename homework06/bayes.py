from math import log


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.known = dict()
        self.y_prob = []

    def fit(self, X, y, y_d):
        """ Fit Naive Bayes classifier according to X, y. """
        k_cnt = len(y_d)
        self.y_prob = [0] * k_cnt
        for i in range(len(y)):
            words = X[i].split()
            # print(words)
            self.y_prob[y_d[y[i]]] += 1
            for word in words:
                if word not in self.known:
                    # print(word)
                    self.known[word] = [0] * (2 * k_cnt + 1)
                # print(self.known[word])
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
        # for key in self.known.keys():
        #    print(key, self.known[key])

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        answer = []
        y_cnt = len(self.y_prob)
        for i in range(len(X)):
            words = X[i].split()
            probs = [log(x) for x in self.y_prob]
            for word in words:
                for j in range(y_cnt):
                    if word not in self.known:
                        continue
                    probs[j] += log(self.known[word][y_cnt + j])
            ind, maxx = 0, probs[0]
            for j in range(1, y_cnt):
                if probs[j] > maxx:
                    maxx = probs[j]
                    ind = j
            print(X[i], probs)
            answer.append(ind)
        return answer

    def score(self, X_test, y_test, y_d):
        """ Returns the mean accuracy on the given test data and labels. """
        correct = 0
        answers = [y_d[y] for y in y_test]
        predictions = self.predict(X_test)
        for i in range(len(y_test)):
            if predictions[i] == answers[i]:
                correct += 1
        return correct / len(y_test)


x = [
    "i love this sandwich",
    "this is an amazing place",
    "i feel very good about these beers",
    "this is my best work",
    "what an awesome view",
    "i do not like this restaurant",
    "i am tired of this stuff",
    "i cant deal with this",
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
x_test = [
    "the beer was good",
    "i do not enjoy my job",
    "i aint feeling dandy today",
    "i feel amazing",
    "gary is a friend of mine",
    "i cant believe im doing this",
]
y_test = ["Positive", "Negative", "Negative", "Positive", "Positive", "Negative"]
y_dict = {"Positive": 0, "Negative": 1}
test = NaiveBayesClassifier(0.1)
test.fit(x, y, y_dict)
# print(test.predict(x_test))
print(test.score(x_test, y_test, y_dict))
