import pandas as pd
import numpy as np
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


df = pd.read_excel("C:/Users/Yash/Downloads/Final_Zomato_Data.xlsx")

def predict_price(Cuisine,Location,Preferred_Price_For_1):

    df = pd.read_excel("C:/Users/Yash/Downloads/Final_Zomato_Data.xlsx")

    Preferred_Price_For_1 = int(Preferred_Price_For_1)

    df = df[["Index","Cuisine","Location","Price_For_One"]]
    z = pd.DataFrame({"Index" : [0], "Cuisine" : Cuisine, "Location" : Location,"Price_For_One": 0})
    df = pd.concat([df,z])

    x = df.drop("Price_For_One",axis = 1)
    y = df["Price_For_One"]

    le = LabelEncoder()
    x["Location"] = le.fit_transform(x["Location"])
    x["Cuisine"] = le.fit_transform(x["Cuisine"])

    xtr,xts,ytr,yts = train_test_split(x,y,test_size = 0.3)
    model = LogisticRegression()
    model.fit(xtr,ytr)
    ypred = model.predict(xts)

    if ypred[-1] > Preferred_Price_For_1:
        return (ypred[-1] - (((ypred[-1] - Preferred_Price_For_1)/100)*70))
    elif ypred[-1] < Preferred_Price_For_1:
        return (ypred[-1] + (((Preferred_Price_For_1 - ypred[-1])/100)*70))
    else:
        return (ypred[-1])

     

def predict_location(Cuisine,Preferred_Location,Preferred_Price_For_1):
    df = pd.read_excel("C:/Users/Yash/Downloads/Final_Zomato_Data.xlsx")

    Preferred_Price_For_1 = int(Preferred_Price_For_1)

    z = pd.DataFrame({"Index" : [0], "Cuisine" : Cuisine, "Location" : Preferred_Location,"Price_For_One":Preferred_Price_For_1})
    df = pd.concat([df,z])

    lst = list(df["Location"].unique())

    dict1 = {}
    for i in range(len(lst)):
        dict1[lst[i]] = i  

    dict2 = {}
    for i in range(len(lst)):
        dict2[i] = lst[i]  

    df["Location"] = df["Location"].apply(lambda x: dict1[x])
    df = df[["Index","Cuisine","Location","Price_For_One"]]

    x = df.drop("Location",axis = 1)
    y = df["Location"]

    le = LabelEncoder()
    x["Cuisine"] = le.fit_transform(x["Cuisine"])
    x["Index"] = 0

    mx = MinMaxScaler()
    x[["Index","Cuisine","Price_For_One"]] = mx.fit_transform(x[["Index","Cuisine","Price_For_One"]])

    xtr,xts,ytr,yts = train_test_split(x,y,test_size = 0.3)
    model = DecisionTreeClassifier()
    model.fit(xtr,ytr)
    ypred = model.predict(xts)

    return dict2[ypred[-1]]


def main():
    st.title("Recommendation Model")

    html_temp = """
    <div style='background-color: red; padding: 10px'>
    <h2 style="color: white; text-align: center;"><b>Zomato Kitchen Ventures: Empowering Your Restaurant Dream</b></h2>
    </div>
    """ 

    css = """
    <style>
    .stApp {
        # background-image: url("data:image/png;base64,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");
        background-size: 500px 500px;
        font-weight: bold;
    }
    </style>
    """

    st.markdown(html_temp + css, unsafe_allow_html=True)

    Cuisine = st.text_input("Cuisine:") 
    Preferred_Price_For_1 = st.text_input("Preferred_Price_For_1:")
    Preferred_Location = st.text_input("Preferred_Location:") 
    
    if st.button("Predict"):

        avg = round(df[(df['Location'] == Preferred_Location)]['Price_For_One'].mean())

        a = df[(df['Location'] == Preferred_Location)]
        Cuis = a[a['Rating'] == a['Rating'].max()]["Cuisine"].to_string().split()[1:]
        Pop_Cuis = " ".join(Cuis)

        Pop_Rest = a[a["Delivery_Review_Number"] == a["Delivery_Review_Number"].max()]["Restaurant_Name"].to_string().split()[1:]
        Most_Popular_Rest = " ".join(Pop_Rest)

        Serve = a[a["Delivery_Review_Number"] == a["Delivery_Review_Number"].max()]["Cuisine"].to_string().split()[1:]
        Serves = " ".join(Serve)

        b = a[(a['Cuisine'] == Cuisine)]
        Rest = b[b["Delivery_Review_Number"] == b["Delivery_Review_Number"].max()]['Restaurant_Name'].to_string().split()[1:]
        Popular_Rest_Serving_Your_Cuisine = ' '.join(Rest)

        Recomm_price = round(predict_price(Cuisine,Preferred_Location,Preferred_Price_For_1))
        Recomm_location = predict_location(Cuisine,Preferred_Location,Preferred_Price_For_1)

        st.success("Average Price for 1:   {}".format(avg))
        st.success("Popular Cuisine:   {}".format(Pop_Cuis))
        st.success("Most Popular Restaurant:  {}".format(Most_Popular_Rest))
        st.success("Serves:  {}".format(Serves))
        st.success("Popular Restaurant that serves your Cuisine: {}".format(Popular_Rest_Serving_Your_Cuisine))
        st.success("Recommended Price:  {}".format(Recomm_price))
        st.success("Recommended Location:  {}".format(Recomm_location))
                
if __name__ == '__main__':
    main()