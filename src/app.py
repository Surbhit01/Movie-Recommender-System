from recommendation import recommendation
import streamlit as st
class app:

    def main():
        st.title('Movie Recommendation System')
        
        
        st.session_state.placeholder = "Show me movies similar to?"
        movie = st.text_input(label = "Enter movie to get similar recommendations",
                              placeholder = st.session_state.placeholder)
        
        btn = st.empty()
        show_recomm_btn = btn.button(label='Show Recommendations')
        
        rc = recommendation()
        rc.load_and_clean_data()
        id = rc.search_title(movie)
        

        if show_recomm_btn:
            btn.empty()    
            df = rc.find_similar_movies(id)
            if df.shape[0] > 0:
                df = df.reset_index()
                print('{} with id: {}'.format(movie,id))
                st.text('Here are some other movie similar to {} which you may like!'.format(movie))
                st.table(df[['title','genres']])
            else:
                st.title('Sorry! no matching recommendations for {} found.'.format(movie))
            #btn.button(label='Show Recommendations')

    if __name__=="__main__":
        main()
        

    
    
    
    
    
    
    
    
    
    