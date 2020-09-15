import pandas as pd
import numpy as np
import time
import math
import matplotlib.pyplot as plt

ATTR_DIR = 'data/genome_scores.csv'
TRAIN_DIR = 'data/train.csv'
TEST_DIR = 'data/test.csv'
GENRE_DIR = 'data/movies.csv'
ATTRIBUTE_SZ = 1128
USER_SZ = 7632
GENRE_SZ = 19

def process_genome_scores():
    i = 0
    data = {}
    print("Processing movie attribute data...")
    GENOME_DATA = pd.read_csv(ATTR_DIR)
    MOVIE_SZ = GENOME_DATA.shape[0]/ATTRIBUTE_SZ
    while(i < MOVIE_SZ):
        movie_data = GENOME_DATA.iloc[i*ATTRIBUTE_SZ:(i+1)*ATTRIBUTE_SZ,2]
        data[GENOME_DATA.iloc[i*ATTRIBUTE_SZ,0]] = movie_data.values.reshape(ATTRIBUTE_SZ,1)
        i += 1
    del GENOME_DATA
    print("Movie data processed!")
    time.sleep(2)
    return data

def process_genres():
    # to hold genre vectors
    genre_data = {}
    # to hold movies under a genre
    genre_movieid = {}
    # to holds genres for movieid
    movie_genres = {}
    
    print("Retrieving genres for movies...")
    GENRE_DATA = pd.read_csv(GENRE_DIR)
    for i in range(GENRE_DATA.shape[0]):
        movieid = GENRE_DATA.iloc[i,0]
        genres = GENRE_DATA.iloc[i,2].split("|")
        genre_vec = convert_genres(genres)
        genre_data[movieid] = genre_vec
        
        movie_genres[movieid] = genres
        
        for genre in genres:
            if genre not in genre_movieid:
                genre_movieid[genre] = [movieid]
            else:
                (genre_movieid[genre]).append(movieid)
                
    del GENRE_DATA
    return genre_data, genre_movieid, movie_genres

def generate_mean_attributes(movieid, genre_movieid, movie_genres, movie_data):
    phi = np.zeros((ATTRIBUTE_SZ,1))
    # get all genres for the movie
    genres = movie_genres[movieid]
    for genre in genres:
        # get all movies with the current genre
        movies = genre_movieid[genre]
        for i in range(len(movies)):
            # get average attributes for all movies of this genre
            if movies[i] in movie_data:
                phi += movie_data[movies[i]]
        phi = phi/len(movies)
    
    phi = phi/len(genres)
    return phi
    
def convert_genres(genres):
    genre_vec = np.zeros((19,1))
    for i in range(len(genres)):
        if(genres[i] == 'Action'):
            genre_vec[0] = 1
        elif(genres[i] == 'Adventure'):
            genre_vec[1] = 1
        elif(genres[i] == 'Animation'):
            genre_vec[2] = 1
        elif(genres[i] == 'Children'):
            genre_vec[3] = 1
        elif(genres[i] == 'Comedy'):
            genre_vec[4] = 1
        elif(genres[i] == 'Crime'):
            genre_vec[5] = 1
        elif(genres[i] == 'Documentary'):
            genre_vec[6] = 1
        elif(genres[i] == 'Drama'):
            genre_vec[7] = 1
        elif(genres[i] == 'Fantasy'):
            genre_vec[8] = 1
        elif(genres[i] == 'Film-Noir'):
            genre_vec[9] = 1
        elif(genres[i] == 'Horror'):
            genre_vec[10] = 1
        elif(genres[i] == 'Musical'):
            genre_vec[11] = 1
        elif(genres[i] == 'Mystery'):
            genre_vec[12] = 1
        elif(genres[i] == 'Romance'):
            genre_vec[13] = 1
        elif(genres[i] == 'Sci-Fi'):
            genre_vec[14] = 1
        elif(genres[i] == 'Thriller'):
            genre_vec[15] = 1
        elif(genres[i] == 'War'):
            genre_vec[16] = 1
        elif(genres[i] == 'Western'):
            genre_vec[17] = 1
        else:
            genre_vec[18] = 1
    return genre_vec

def train_user_model(data, W, aux_data, eta, lam):
    userid, movieid, rating = data
    movie_data, genre_data, genre_movieid, ratings_mean, movie_genres = aux_data

    # if new user, then create an entry to weight matrix
    if userid not in W:
        W[userid] = np.zeros((ATTRIBUTE_SZ+GENRE_SZ+1,1))

    # if movie does not have genome scores, generate average attributes based on genres
    if movieid not in movie_data:
        phi = generate_mean_attributes(movieid, genre_movieid, movie_genres, movie_data)
        # phi = np.zeros((ATTRIBUTE_SZ,1))
    else:
        # get feature vector for movie
        phi = movie_data[movieid]

    phi = np.vstack((1,phi,genre_data[movieid]))
    phi = phi/np.linalg.norm(phi)    

    # get linear regression weights for user
    w = W[userid]
    # update regression weights for user
    w = w + eta*((rating - (w.T).dot(phi))*phi - lam*w)
    # update the weight matrix
    W[userid] = w
    # update movie mean ratings
    if movieid not in ratings_mean:
        ratings_mean[movieid] = np.array([rating, 1])
    else:
        ratings_mean[movieid][0] += rating
        ratings_mean[movieid][1] += 1

 
def train_model(aux_data, eta, epochs, lam = 0):
    # initialise dict to hold weights for users
    W = {}
    # initialise dict to hold movie mean ratings
    ratings_mean = {}
    
    movie_data, genre_data, genre_movieid, movie_genres = aux_data
    aux_data = [movie_data, genre_data, genre_movieid, ratings_mean, movie_genres]
    
    train_data = pd.read_csv('data/split_train.csv')
    train_data = train_data.values
    time.sleep(1)
    print("Training model:")
    epoch = 0
    while(epoch < epochs):
        print("Epoch No: %d" % (epoch))
        for i in range(train_data.shape[0]):
            data = train_data[i,:]
            train_user_model(data, W, aux_data, eta, lam)
            if(i%400000 == 0):
                print("Progress: %.2f percent" %(i/train_data.shape[0]*100))

        epoch += 1

    mean = np.mean(train_data[:,2])
    del train_data
    return W, ratings_mean, mean

def predict_rating(userid, movieid, W, aux_data):
    movie_data, genre_data, genre_movieid, movie_genres, ratings_mean, mean = aux_data
    # if user not encountered during training
    if userid not in W:
        # if movie not encountered during training predict mean rating
        if movieid not in ratings_mean:
            pred = mean
        else:
        # movie encountered, predict corresponding mean rating
            pred = ratings_mean[movieid][0]/ratings_mean[movieid][1]
    else:
        w = W[userid]
        if movieid not in movie_data:
            # if movie does not have genome scores, use mean attributes
            phi = generate_mean_attributes(movieid, genre_movieid, movie_genres, movie_data)
            phi = np.vstack((1,phi,genre_data[movieid]))
            phi = phi/np.linalg.norm(phi)            
            if movieid in ratings_mean:
                # if movie encountered during training, take weighted average 
                pred = 0.7*(w.T).dot(phi) + 0.3*ratings_mean[movieid][0]/ratings_mean[movieid][1]
            else:
                # if movie not encountered during training, predict based on mean attributes
                pred = (w.T).dot(phi)
                
# =============================================================================
#             # if movie not encountered during training predict mean rating
#             phi = np.zeros((ATTRIBUTE_SZ,1))
#             phi = np.vstack((1,phi,genre_data[movieid]))
#             phi = phi/np.linalg.norm(phi)
#             if movieid not in ratings_mean:
#                 pred = (w.T).dot(phi)
#             else:
#                 pred = 0.4*(w.T).dot(phi) + 0.6*ratings_mean[movieid][0]/ratings_mean[movieid][1]
# =============================================================================
        else:
            phi = movie_data[movieid]
            phi = np.vstack((1,phi,genre_data[movieid]))
            phi = phi/np.linalg.norm(phi)
            pred = (w.T).dot(phi)

    pred = round(float(pred),1)

    if pred > 5.0:
        pred = 5.0
    elif pred < 0.5:
        pred = 0.5

    return pred

def predictions(W, aux_data):   
  #  movie_data, genre_data, genre_movieid, movie_genres, ratings_mean, mean = aux_data
    
    print("Beginning test data evaluation...")
    test_data = pd.read_csv(TEST_DIR)
    test_data = test_data.values
    pred = np.zeros((test_data.shape[0],1))
    idd = np.arange(0, test_data.shape[0],1)
    for i in range(test_data.shape[0]):
        ids = test_data[i,:]
        pred[i] = predict_rating(ids[0], ids[1], W, aux_data)
        if(i%100000 == 0):
            print("Progress: %.2f percent" %(i/test_data.shape[0]*100))

    df = pd.DataFrame(idd, columns = ['Id'])
    df['Prediction'] = pred
    df.to_csv('data/results.csv', index=False)
    del test_data

def split_pred(W, aux_data):
    print("Beginning test data evaluation...")
    test_data = pd.read_csv('data/split_test.csv')
    test_data = test_data.values
    error = 0; total = 0;
    for i in range(test_data.shape[0]):
        ids = test_data[i,:]
        pred = predict_rating(ids[0], ids[1], W, aux_data)
        error += (pred-ids[2])**2
        total += 1
        if(i%400000 == 0):
            print("Progress: %.2f percent" %(i/test_data.shape[0]*100))
    return error/total



def main():
    # get attribute relevance scores for each movie
    movie_data = process_genome_scores()
    genre_data, genre_movieid, movie_genres = process_genres()
    aux_data = [movie_data, genre_data, genre_movieid, movie_genres]
    W, ratings_mean, mean = train_model(aux_data, 0.5, 4)
    aux_data = [movie_data, genre_data, genre_movieid, movie_genres, ratings_mean, mean]
    print("MSE = %f" % (split_pred(W, movie_data, genre_data, ratings_mean, mean)))
    #predictions(W, aux_data)

if __name__ == '__main__':
    main()
