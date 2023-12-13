# GitSphere - GitHub Insights Web Service
## Introduction

Welcome to **GitSphere**, a project aimed at empowering developers with data-driven insights and analytics for their GitHub repositories.

**GitHub API** plays a vital role in the development of this application, it is an example of **REST APIs**.

This project is part of the portfolio for **Holberton School**, completed on 12/12/2023. Find the project repository on [GitHub](https://github.com/valariembithe/GitSphere).

This is a group project done by 2 aspiring software engineers. Here are the links to their LinkedIn profiles.
- [Valarie Muema](https://www.linkedin.com/in/valarie-muema-549403231/)
- [Jimmy Mutuku](https://www.linkedin.com/in/jimmymutuku/)

Here is the link to the [deployed website]().

## Installation

To use Gitsphere, there are `commands` that are key and need to be used to experience the amazing of this application.
1. Open a browser, and type the URL for this application in the search button and press **Enter**.
2. This will prompt the application to navigate to the **home** page, route '/'
  - This page return a welcome message
    > Welcome to GitSphere - Github Insights Web Service!
3. To use this web application, the user has to **give permission** to the application and will be prompted to **Login with GitHub**. 

## Usage
Now that youn have granted permissions to **GitSphere** and **Logged in using your GitHub account**, you can explore the features of this application that is geared to empower developers with data-driven insights and analytics for their GitHub repositories. 
1. At the end of the URLs '/' path, add an endpoint `user`.
   - This endpoint `user` returns the authenticated **user's profile details** including the **name, bio, location, followers and following**.
2. Endpoint `/user/<username>`
   - This endpoint returns the user profile details in a template. One should replace the parameter `username` with an existing GitHub username.
3. Endpoint `/user/<username>/repositories`
   - This endpoint returns the repositories for the specified GitHub user using their username. 
4. Endpoint `/logout`
   - This endpoint logout a user and clears out the session stored. This makes it more secure to use the application.

## Contributing
This project was done by 2 software engineers which is part of the **Holberton School - Building your porfolio project**.

Here are the links to each contributor's Github page.
- [Valarie Muema](https://github.com/valariembithe).
- [Jimmy Mutuku](https://github.com/SirJimKe)

## Related Projects
There are other related projects that we have worked on as a team.
- [AirBnB_Clone](https://github.com/valariembithe/AirBnB_clone).
  - Written in Python, HTML and CSS.
- [Simple Shell](https://github.com/valariembithe/simple_shell).
  - Written in C#.

## Licensing

This project is original and a product of the 2 software engineers listed in this repository. 
