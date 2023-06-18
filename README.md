# foodstock-backend

Foodstock is a web application that allows you to manage your food stock. It is composed of a frontend and a backend. This is the backend part.

## Architecture
The backend is build using [FastAPI](https://fastapi.tiangolo.com/). It is a Python framework that allows you to build APIs very quickly. It is based on [Starlette](https://www.starlette.io/) and [Pydantic](https://pydantic-docs.helpmanual.io/).

I chose to use FastAPI because it is very fast and easy to use. It is also very well documented and has a lot of examples. It also comes with Swagger UI to document the API, accessible at '/docs'.

The frontend and backend are separated in two different repositories. The backend is available [here](https://github.com/food-stock/foodstock-backend).

 I wanted them to be separated because I wanted to be able to change the frontend without changing the backend and vice versa.


## Features
- [x] Basic functions
- [ ] Authentication
- [ ] Endpoints specific for each user using their id
- [ ] Secure the API
