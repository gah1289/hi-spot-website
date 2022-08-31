# Project Title

Hi Spot Condominium Website
https://hispot-website.herokuapp.com/


## Description

A website made for Hi Spot Condominium Association on Lake Winnipesaukee, NH. The goal is to allow residents to access information about the condo association and pay monthly invoices online.

## Database Schema

![image info](./Hi-Spot%20Schema.png)

## User flow

### Accessible to all

***Home Page (Accessible to all):***
- Hi-spot Logo and weather app for Laconia, NH at the top of the page
  - Weather app made via JS using OpenWeatherMap API (https://openweathermap.org/api)
- Nav bar with grid that takes user back to home page and dropdown menu showing links to:
  - Photo Gallery 
  - Resident Login
- Brief description of the condo 
- Photo: aerial view of the condo
- Footer with link to FaceBook page and address

***Photo Gallery:***
- View photos of Hi-spot, be able to click and enlarge, see who added the photo

***User Login***:
- User can log in with username and password
- Link to register if user does not have an account
- If password/username is wrong, error message appears

***Register***:
- User must enter the following information to register:
  - First name
  - Last Name
  - email
  - Unit number (must be 1-18)
  - Username (must be unique)
  - Password (must be at least 6 characters). Will be hashed for security
  - Confirm Password

### Accessible to Logged in Users

***Condo Events Page***
- Ability to view upcoming events. 
- If event date is past current date, it moves to past events list.
- Each event shows:
  - Title
  - Description
  - Date
  - Start time
  - End Time
  - Who added the event

  - *Board members Only:*
    - Can add event
    - Reschedule event
      - event description changes to "This event has been rescheduled" in yellow text
    - Cancel event
      - event description changes to "This event has been cancelled" in red text
      - All event details are crossed out
    - Delete event
      - Remove event from list entirely

***Condo Docs***
- Ability to download condo docs individually or as a zip file

***Pay Invoice***
- Pay online (ability to pay their monthly invoices via credit card)
  - Uses Stripe API (https://stripe.com/docs/api)
  - Stripe API handles all sensitive user information and ensures user protection
- Handles and shows errors for missing fields, wrong numbers, invalid numbers, declined cards bad expiration dates
- Flashes message when payment is successul


***Contact***
- View board contact information
- Email board 

*Edit Board (Accessible to Admin Only)*
- Ability to edit board members

***Account (dropdown menu)***
- Edit account information
- Change Password
- Log out




## To do:
  - Compensate for percentage Stripe takes out
  - Approval for user registration
  - Ensure security
  - Add ability to pay with bank routing number
  - Chang Stripe API information when live
    - Bank information
    - Take out of test mode
  
  ## Acknowledgements 
- Rahul Sharma, Springboard Mentor
- CSS:
  - https://www.w3schools.com/howto/howto_css_hide_scrollbars.asp
  -  https://dev.to/khush2706/frosted-glass-effect-in-css-27p4 (frosted glass effect)
  -  https://css-irl.info/animating-underlines/ (navbar hover effect)
  -  https://css-tricks.com/almanac/selectors/p/placeholder/ 
  -   https://stackoverflow.com/questions/61462583/html-input-css-background-color-not-applied 
  -   https://stackoverflow.com/questions/2781549/removing-input-background-colour-for-chrome-autocomplete 
  -   https://codepen.io/maheshambure21/pen/QwXaRw 
- HTML
  - https://codepen.io/SeedThemes/pen/ZpmEzx - footer
  - Cancel event modal https://getbootstrap.com/docs/5.2/components/modal/#how-it-works
  - loon by Yi Chen from https://thenounproject.com/browse/icons/term/loon/" Noun Project
  - https://www.compass.com/listing/277-weirs-boulevard-unit-13-laconia-nh-03246/958522483031257345/ Hi Spot Description Text
- Python
  - Select Field default values: https://lightrun.com/answers/wtforms-flask-wtf-add-empty-option-in-selectfield   
  - https://stackoverflow.com/questions/20457038/how-to-round-to-2-decimals-with-python  

## Frameworks/Libraries
- Bootstrap 
- JQuery
- FontAwesome
- Google Fonts
- Axios
- Flask
- SQLAlchemy

## Databases
- Postgresql

## APIs
- OpenWeatherMap
- Stripe

## Contact
- Gabriela McCarthy
- gah1289@gmail.com