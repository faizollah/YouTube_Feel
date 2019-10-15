# YouTube Feel - Analysis of Videos' Comments
------
This project is hosted on free plan of Heroku. It goes to sleep after certain time of inactivity. Please be patient when visiting the website.

This application was implemented using Python's Flask framework.

Upon signing up, which is implemented using Firebase, the user is directed to the payment page. The payment is processed using Stripe.

After the payment is successful, a token and email address is stored in Firestore as a record. 

The user is then directed to the page where a link to YouTube video is required. The application pulls the video's comments and performs sentiment analysis on the data. The result is then displayed in form of positive and negative percentage.

At this point it only shows the percentage. We are working on providing more analysis like wordcloud figure.

This work was done by Ali Feizollah individually.
