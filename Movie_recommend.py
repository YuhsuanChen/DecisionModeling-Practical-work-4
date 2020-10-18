import csv
import math

import scipy as scipy
import scipy.stats

Critiques = {}
CritiqueList = []
MovieList = []

with open("movie_score.csv", newline='') as csvFile:
    data = csv.reader(csvFile, delimiter=',')
    for row in data:
        Critiques = dict((rows[0], (rows[1], rows[2], rows[3], rows[4], rows[5], rows[6])) for rows in data)  #
with open("movie_score.csv", newline='') as csvFile:
    data = csv.reader(csvFile, delimiter=',')
    header = next(data)
    for name in header:
        MovieList.append(name)

"""# (a)  Manhattan distance or an Euclidean distance."""


def sim_distanceManhattan(person1, person2):
    Distance = 0
    for i in range(len(person1)):
        if not (person1[i] == " " or person2[i] == " "):
            Distance = Distance + (abs(float(person1[i]) - float(person2[i])))
    return Distance


def sim_distanceEuclidienne(person1, person2):
    Distance = 0
    for i in range(len(person1)):
        if not (person1[i] == " " or person2[i] == " "):
            Distance = Distance + (float(person1[i]) - float(person2[i])) ** 2
    return math.sqrt(Distance)


print("Manhattan distance", sim_distanceManhattan(Critiques['Lisa Rose'], Critiques['Gene Seymour']))
print("Euclidienne distance", sim_distanceEuclidienne(Critiques['Lisa Rose'], Critiques['Gene Seymour']))

for key in Critiques.keys():
    CritiqueList.append(key)

"""# (b)  NearestNeighbor"""


def computeNearestNeighbor(nouveauCritique, CritiqueList):
    distances = []
    for c in CritiqueList:
        if not c == nouveauCritique:
            distance = sim_distanceManhattan(Critiques[c], Critiques[nouveauCritique])
            distances.append((distance, c))
    return distances


print("Nearest Neighbor of Toby:", computeNearestNeighbor('Toby', CritiqueList))

""" (c) Step 1 : For each movie a not seen by Anne, compute the quantities"""


def Weighted_score(nouveauCritique, movieName):
    PersonName = CritiqueList
    score_index = MovieList.index(movieName)
    # Get the score of the movie from individual
    score = []  # the score for movieName from each individual
    for n in CritiqueList:  # each name in the dictionary
        if (Critiques.get(n)[score_index - 1]) != " ":
            score.append((float(Critiques.get(n)[score_index - 1])))  # get the value in dictionary
        else:
            score.append(0)

    name_weight = computeNearestNeighbor(nouveauCritique, PersonName)
    weight = []

    for n_w in name_weight:
        weight.append(n_w[0])

    Total = 0
    S = 0
    global_score = 0
    for critique_index in range(len(score) - 1):
        Total = Total + (score[critique_index] / (1 + weight[critique_index]))  # Total(a)
        S = S + (1 / (1 + weight[critique_index]))  # S(a)
        global_score = Total / S
    return global_score
    # "Total: ", Total
    # "S(Anne): ", S
    # "S'(a): ", Total / S


""" (c) Step 2 : The movie to recommend to Anne will be the movie with the highest global score s'(a)"""


def Best_recommend(Person, movie_list):
    Recommend = movie_list[0]
    output = ""
    for i in range(len(movie_list)):
        output += "Score of " + str(movie_list[i]) + " is " + str(Weighted_score(Person, movie_list[i])) + ".  "
        if i > 0 and Weighted_score(Person, movie_list[i]) > Weighted_score(Person, movie_list[i - 1]) and Weighted_score(Person, movie_list[i]) > Weighted_score(Person, movie_list[0]):
            Recommend = movie_list[i]
    print("[Best recommend]", output + " \nThus, recommend movie with weighted score for ", Person, " is ",
          Recommend + "\n")
    return Recommend


def Weighted_score_withExp(nouveauCritique, movieName):
    PersonName = CritiqueList
    score_index = MovieList.index(movieName)
    # Get the score of the movie from individual
    score = []  # the score for movieName from each individual
    for n in CritiqueList:  # each name in the dictionary
        if (Critiques.get(n)[score_index - 1]) != " ":
            score.append((float(Critiques.get(n)[score_index - 1])))  # get the value in dictionary
        else:
            score.append(0)

    name_weight = computeNearestNeighbor(nouveauCritique, PersonName)
    weight = []

    for n_w in name_weight:
        weight.append(n_w[0])

    Total = 0
    S = 0
    global_score = 0
    for critique_index in range(len(score) - 1):
        Total = Total + (score[critique_index] * math.exp(-weight[critique_index]))  # Total(a) ~ exponential value
        S = S + math.exp(-weight[critique_index])  # exponential value
        global_score = Total / S
    return global_score


def BestrecommendwithExp(Person, movie_list):
    Recommend = movie_list[0]
    output = ""
    for i in range(len(movie_list)):
        output += "Score of " + str(movie_list[i]) + " is " + str(Weighted_score_withExp(Person, movie_list[i])) + ".  "
        if i > 0 and Weighted_score_withExp(Person, movie_list[i]) > Weighted_score_withExp(Person, movie_list[i - 1]) and Weighted_score_withExp(Person, movie_list[i]) > Weighted_score_withExp(Person, movie_list[0]):
            Recommend = movie_list[i]
    print("[Exp best recommendation]", output, " \nThus, recommend movie with exponential weighted for ", Person,
          " is ", Recommend + "\n")
    return Recommend


Anne_have_not_seen = ['Night', 'Snakes', 'Superman']
Best_recommend('Anne', Anne_have_not_seen)
BestrecommendwithExp('Anne', Anne_have_not_seen)

Michael_have_not_seen = ['Luck', 'Dupree']
Best_recommend('Michael Phillips', Michael_have_not_seen)
BestrecommendwithExp('Michael Phillips', Anne_have_not_seen)

"""(d) Pearson correlation coefficient"""


def Pearson_similarity(person1, person2):
    n = 0
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    for i in range(len(person1)):
        if not (person1[i] == " " or person2[i] == " "):
            n += 1
            x = float(person1[i])
            y = float(person2[i])
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += x ** 2
            sum_y2 += y ** 2
    denominator = math.sqrt(sum_x2 - (sum_x ** 2) / n) * math.sqrt(sum_y2 - (sum_y ** 2) / n)
    if denominator == 0:
        return 0
    else:
        return (sum_xy - (sum_x * sum_y) / n) / denominator


def Pearson_NearestNeighbor(nouveauCritique, CritiqueList):
    distances = []
    for c in CritiqueList:
        if not c == nouveauCritique:
            distance = Pearson_similarity(Critiques[c], Critiques[nouveauCritique])
            distances.append((distance, c))
    return distances


def Pearson_weighted_score(Person, movie):
    PersonName = CritiqueList
    score_index = MovieList.index(movie)
    score = []  # the score for movieName from each individual
    for n in CritiqueList:  # each name in the dictionary
        if (Critiques.get(n)[score_index - 1]) != " ":
            score.append((float(Critiques.get(n)[score_index - 1])))  # get the value in dictionary
        else:
            score.append(0)

    name_weight = Pearson_NearestNeighbor(Person, PersonName)
    weight = []

    for n_w in name_weight:
        weight.append(n_w[0])

    Total = 0
    S = 0
    global_score = 0
    for critique_index in range(len(score) - 1):
        Total = Total + (score[critique_index] * (2 + weight[critique_index]))  # Total(a)
        S = S + (2 + weight[critique_index])  # exponential value
        global_score = Total / S
    return global_score


def PearsonRecommend(Person, movie_list):
    Recommend = movie_list[0]
    output = ""
    for i in range(len(movie_list)):
        output += "Score of " + str(movie_list[i]) + " is " + str(Pearson_weighted_score(Person, movie_list[i])) + ".  "
        if i > 0 and Pearson_weighted_score(Person, movie_list[i]) > Pearson_weighted_score(Person, movie_list[i - 1]) and Pearson_weighted_score(Person, movie_list[i]) > Pearson_weighted_score(Person, movie_list[0]):
            Recommend = movie_list[i]

    print("[Pearson]", output + " \nThus, recommend movie with Pearson weighted for ", Person, " is ", Recommend + "\n")
    return Recommend


PearsonRecommend('Anne', Anne_have_not_seen)

"""(e) CosineRecommend"""


def Cosine_similarity(person1, person2):
    n = 0
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    for i in range(len(person1)):
        if not (person1[i] == " " or person2[i] == " "):
            n += 1
            x = float(person1[i])
            y = float(person2[i])
            sum_xy += x * y
            sum_x2 += x ** 2
            sum_y2 += y ** 2
    denominator = math.sqrt(sum_x2) * math.sqrt(sum_y2)
    if denominator == 0:
        return 0
    else:
        return sum_xy / denominator


def Cosine_NearestNeighbor(nouveauCritique, CritiqueList):
    distances = []
    for c in CritiqueList:
        if not c == nouveauCritique:
            distance = Cosine_similarity(Critiques[c], Critiques[nouveauCritique])
            distances.append((distance, c))
    return distances


def Cosine_weighted_score(Person, movie):
    PersonName = CritiqueList
    score_index = MovieList.index(movie)
    score = []  # the score for movieName from each individual
    for n in CritiqueList:  # each name in the dictionary
        if (Critiques.get(n)[score_index - 1]) != " ":
            score.append((float(Critiques.get(n)[score_index - 1])))  # get the value in dictionary
        else:
            score.append(0)

    name_weight = Cosine_NearestNeighbor(Person, PersonName)
    weight = []

    for n_w in name_weight:
        weight.append(n_w[0])

    Total = 0
    S = 0
    global_score = 0
    for critique_index in range(len(score) - 1):
        Total = Total + (score[critique_index] * (2 + weight[critique_index]))  # Total(a)
        S = S + (2 + weight[critique_index])  # exponential value
        global_score = Total / S
    return global_score


def Cosine_Recommend(Person, movie_list):
    Recommend = movie_list[0]
    output = ""
    for i in range(len(movie_list)):
        output += "Score of " + str(movie_list[i]) + " is " + str(Cosine_weighted_score(Person, movie_list[i])) + ".  "
        if i > 0 and Cosine_weighted_score(Person, movie_list[i]) > Cosine_weighted_score(Person, movie_list[i - 1]) and Cosine_weighted_score(Person, movie_list[i]) > Cosine_weighted_score(Person, movie_list[0]):
            Recommend = movie_list[i]

    print("[Cosine]", output + " \nThus, recommend movie with Cosine weighted for ", Person, " is ", Recommend + "\n")
    return Recommend


Cosine_Recommend('Anne', Anne_have_not_seen)
