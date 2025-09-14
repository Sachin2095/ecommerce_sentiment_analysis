from scripts.data_preprocessing import CleanReview
import pickle
import logging 
import os 
os.chdir('/Ecommerce Sentiment Analysis')
# basic Structure of Logging
file_name="User logs"
logging.basicConfig(
    filename=f"logs/{file_name}.log",
    level=logging.INFO,
    format="%(asctime)s-%(levelname)s-%(message)s",
    filemode="a"
)
# creating object of Clean review

cr=CleanReview()

# preprocess the text 
def AnalysisText(text):
    logging.info(f"the given review is {text} .")
    try:
       logging.info("Processing has started")
       text=cr.clean_html(text)
       logging.info("clean html has completed")
       text=cr.convert_lower(text)
       logging.info("text has been converted into lower case ")
       text=cr.remove_special(text)
       logging.info("Special charactors has been removed")
       text=cr.remove_stopwords(text)
       logging.info("Stopwords has been removed")
       text=cr.stem_words(text)
       logging.info("Stemmetization has been done.")
       text=cr.join_back(text)
       logging.info("Text has been joined back")
       text=cr.remove_emojis(text)
       logging.info("Emojis has been removed.")
       logging.info("Preprocessing has been ended.")      

       # import the model 
       logging.info("model is loading .")
       with open("mlartifacts\\0\\models\\m-932c78f239a24b209319539074b9a024\\artifacts\\model.pkl", "rb") as f:
           model = pickle.load(f)       
       
       # make predicts 
       logging.info("Model is making predictions")
       result=model.predict([text])       
       
       # making result into text 
       logging.info("Predict is Ready .")
       if result==1 :
           return 'The review is Positive. The Product is Quite Awesome .'       
       elif result==-1 :
           return 'The review is Negative.This product needs to be removed .'       
       else :
           return 'The  review is Ok. This product is still needs some improvements.'
    except Exception as e:
        logging.error(f"Error in AnalysisText: {str(e)}")
        raise RuntimeError("something went wrong") from e
    

