# csci450-final-project-frontend

This is the Vue.js frontend for the CSCI 450 final project, STEManager - a STEM camp registration
system. The project is designed to work with a backend API that provides the necessary data and functionality for the application. The frontend is built using Vue.js, a progressive JavaScript framework for building user interfaces.


## Project Setup
To run it locally, first install dependencies by opening your terminal, navigating to this folder, and running:

```sh
npm install
```
Next, you need to set up the environment variables. Create a `.env` file in the root directory of the project and add the following variables, making sure to replace {YOUR_BACKEND_URL_HERE}:

```env
VITE_API_URL={YOUR_BACKEND_URL_HERE}
VITE_COPYRIGHT_NAME=Luke Ertzberger, Samuel Etzkorn, Constantine Ewan, and Rachel Georges
```

### Run The Project
If you want to run the project locally, you can use the following command to start a local server that will automatically reload when you make changes to the code:
```sh
npm run dev
```

