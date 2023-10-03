Flask Web Application 
# Athlete Management Application
#### Video Demo:  <https://youtu.be/_mJCe3yJ63k>
#### Description:
This is a very simple version of what I wish to build one day. This Flask application simply
allows a coach to register a coach profile and create athletes to list on their profile.
The coach is then able to edit the profile of their registered athletes. This profile is viewable by the coach, as well
as the athlete who will be provided login details by their coach.

In this Flask application, the main objective is to create a streamlined sports coaching management system, facilitating coach and athlete interactions. The application employs various functions to achieve this goal.

The `landing()` function sets the initial page users encounter upon accessing the application. Acting as a welcome gateway, it sets the tone for the user experience. The application offers a registration process for coaches through the `registercoach()` function. Here, coaches input their desired username and password. The function ensures these entries are valid and unique before hashing the password for secure storage in the database.

For athlete registration, the `registerathlete()` function serves a similar purpose. It authenticates the athlete's credentials and associates them with a coach. Athletes are then able to access their profiles using the `athletelogin()` function. This function validates the athlete's login credentials and fetches their profile data from the database, rendering it on their landing page.

On the other hand, the `coachlogin()` function allows coaches to log in, subsequently redirecting them to a landing page displaying their athletes' usernames. Should any information need updating, the `editathleteform()` function allows coaches to modify athlete profiles by altering relevant details and storing these changes securely in the database.

Lastly, the application includes auxiliary features, like a `logout()` function for terminating sessions and a `contact()` function for providing a point of communication. All these functions collectively contribute to a coherent user experience, simplifying the management of coach and athlete profiles.

To enhance the application, it is imperative to address security concerns. Implementing robust measures against SQL injection and bolstering session security is crucial. Additionally, input validation must be comprehensive to guarantee data integrity and consistency. With these improvements, the application can offer a seamless and secure platform for coaches and athletes to interact effectively.


Goals:
Later on, once I understand a bit more, I will add to this application. I intend to add a section for more specific
athlete data such as training data and session tracking. I need to fix some of the routing and possibly add to the security. Also a 'remove athlete' function needs to be added to the coach's main page.
