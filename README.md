# Cooking For Two

Cooking is a hobby and necessity that can be challenging to fit into a busy lifestyle.  This website will aim to help give new ideas to two-person households (or could be doubled-up for a four-person household) and serve as a repository – essentially a personalised online cooking book – that users can upload new recipes to, modify or delete these new recipes, and buy the necessary kitchen equipment needed to cook the recipes.

The live website can be viewed [here](https://cooking-for-two.herokuapp.com/).

## Contents:
[UX](#ux)<br>
[Structure](#structure)<br>
[Database Design](#database-design)<br>
[Technologies Used](#technologies-used)<br>
[Testing](#testing)<br>
[Deployment](#deployment)<br>
[Credits](#credits)

-----

## UX
User Stories

As a user of the site, I want:
- to be able to easily view a range of dishes and their recipes.
- to clearly understand the layout of the website and move about easily.
- to be able to view the website on any device for convenience (e.g. on the user's phone while cooking)
- to be able to create my own recipes on the website and store them there.

As an administrator of the site, I want:
- to be able to update or delete any recipe on the site, to allow quality control.

As a business owner of the site, I want:
- users to sign up to the website to encourage them to use it more often.
- users who are registered and signed in to easily create recipes and use the site, thus encouraging repeat visits.
- users to be encouraged, but not pushed, to visit the shop page to buy items through the website.

## Structure
### Overview of site and page structure, including functionality and purpose:
#### Home Page
- Header for easy navigation between pages of the site.
- Flashed messages appear to left of navigation bar for consistency throughout site.
- Welcome title with 'Browse Recipes' and 'Register' buttons for simplicity and clarity
- Dish Cards for key information about a dish - region, title, creator, 'More' button to register

#### Register Page/ Login Page
- Username input: text input box
- Password input: text input box
- Submit Button: to send information to back-end
- Sign-in link: if users already have a profile

#### Profile Page
- Similar structure to Home Page to ensure consistency across website to improve UX
- Welcome message now has "User's Homepage" to indicate logged in
- Search bar to allow user 


(description of each page, and image)

Skeleton (wireframes)

Surface (colour and styling, language & tone, Styling considerations)

-----

## Database design
(dbdiagram.io)
    Indexes
        recipes
    Queries
        browsing
        users
        searching
        uploading
        deletion

-----

## Technologies used
    Languages
    Libraries
        Bootstrap
        Font Awesome
        Google Fonts
        jQuery
        Flask
        Werkzeug (manage user management integrity)
    Editors
        GitHub
        GitPod
        dbDiagram
        Balsamiq
    Tools
        Flask-Paginate
        TinyPNG/ TinyJPG
        Coolers - colour palette generation
        Image colour picker (from logo)
        Real Favicon Generator
        Am I Responsive?
    Database Management
        MongoDB
    Deployment Platform
        Heroku

-----

## Testing

Automatic Testing

User Stories Testing
As a user of the site, I want:
- to be able to easily view a range of dishes and their recipes.
    Included all dishes available on home page, to allow instant access to see what range is available.
- to clearly understand the layout of the website and move about easily.
    Included navbar and instructions for website to allow ease of use, and also ensured that Creating, Reading, Updating and Deleting recipes are within 2 pages of user's profile page to allow convenience.
- to be able to view the website on any device for convenience (e.g. on the user's phone while cooking)
    Ensured that the website was fully responsive and would work on all common devices through Chrome's Dev Tools.
- to be able to create my own recipes on the website and store them there.
    Included Create functionality once user logged in to allow creation of custom recipe.

As an administrator of the site, I want:
- to be able to update or delete any recipe on the site, to allow quality control.
    Included admin rights to allow updating or deleting rights to admin user.

As a business owner of the site, I want:
- users to sign up to the website to encourage them to use it more often.
    Ensured that only registered and signed-in users can access the actual recipes and ingredients of dishes.
- users who are registered and signed in to easily create recipes and use the site, thus encouraging repeat visits.
    Included navbar and instructions for website to allow ease of use, and also ensured that Creating, Reading, Updating and Deleting recipes are within 2 pages of user's profile page to allow convenience.
- users to be encouraged, but not pushed, to visit the shop page to buy items through the website.
    Included 'Shop' page which 'Recipe' page has links to, so users can easily be taken within 2 clicks to a shopping site to purchase their necessary equipment for the recipe.

-----

## Deployment

-----

## Credits