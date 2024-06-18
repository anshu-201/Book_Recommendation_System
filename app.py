from flask import Flask,render_template,request
import pickle
import numpy as np

import os
import pickle

# Get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Combine the current directory path with the file name
file_path = os.path.join(current_dir, 'model', 'popular.pkl')

# Load the pickle file
with open(file_path, 'rb') as file:
    popular_df = pickle.load(file)

# Combine the current directory path with the file name
pt_path = os.path.join(current_dir, 'model', 'pt.pkl')
books_path = os.path.join(current_dir, 'model', 'books.pkl')
similarity_scores_path = os.path.join(current_dir, 'model', 'similarity_scores.pkl')

# Load the pickle files
pt = pickle.load(open(pt_path, 'rb'))
books = pickle.load(open(books_path, 'rb'))
similarity_scores = pickle.load(open(similarity_scores_path, 'rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    
    # Initialize index to a default value
    index = -1  
    
    # Check if pt.index is not empty
    if len(pt.index) > 0:
        # Find the index of user_input in pt.index
        index_array = np.where(pt.index == user_input)[0]
        # Check if user_input exists in pt.index
        if len(index_array) > 0:
            index = index_array[0]
        else:
            # Handle the case where user_input is not found in pt.index
            pass
    else:
        # Handle the case where pt.index is empty
        pass
    
    # Rest of your code to generate recommendations

    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)