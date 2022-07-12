# Python (FastAPI, Pymotyc) backend and MongoDB in Docker Compose

This repository is an example project that shows how to:

1. Setup and run `MongoDB` container.
2. Create some models and CRUD operations for `MongoDB` it in `Pymotyc` - a simple yet powerful `Python` library, but with funny quirks.
3. Create a backend in `FastAPI` - another `Python` library.
4. Wrap it all in `Docker Compose`.

## How to run it

1. `git clone` the repository and `cd` in its root directory.
2. Create `.env` file. Copy and paste the content of `sample.env` inside the `.env`. Edit some fields if you want.
3. Run `docker compose up --build` and wait for a moment.
4. Go to your browser and type `127.0.0.1:8000/docs` in address line.
5. Feel free to play around.

## Explanation (long and painful)

### The Docker part

`.env` file acts as a configuration file that can store sensitive information. It's not recommended to share it anywhere.

`sample.env` is just an example `.env` for you to better understand what fields there are.

`docker` folder contains everything to build and run containers.

`docker/Dockerfile` specifically builds Python backend by installing libraries listed in `docker/requirements.txt`, then copying everything from the `backend` folder.

In `docker-compose.yml` you can see configurations for both database and backend container. The file reads environment variables from `.env` (notice the `${VAR}` syntax). It also loads variables listed there to backend container (`env_file`). Mongo has its storage exposed, so you can move it to another machine, preserving the data.

All containers share the same local network, so they can contact with each other via their container names (local DNS will resolve those automagically). Note that ports `8000` and `21017` are exposed on host machine, and you can connect to them from your host machine using `localhost` (so you can run the backend locally, without Docker). HOWEVER, any container's `localhost` refers to the container itself, so to set up container interactions, ALWAYS use container names. ~~Yes, I spent 2 days on that, and it's funny.~~

### The backend part

Core libraries are [Pymotyc](https://github.com/AntonOvsyannikov/pymotyc) and [FastAPI](https://fastapi.tiangolo.com/).

`backend` is quite straightforward, you can read it on your own if you're proficient with Python - there aren't many super-advanced concepts.

Anyway, the structure is simple:

`backend.main` configures the application, connects to database, setups error handling, and includes routers.

`backend.models` is what is stored in the database. Thanks to [Pydantic](https://pydantic-docs.helpmanual.io/), fields are validated.

`backend.routers` are used to separate huge API in smaller parts and function sort of like smaller applications. Routers make use of path operations in URI and can be included by main app to unite it all together.

`backend.storage` is simply a Mongo database with its own collections that can be configured. Thanks to `Pymotyc`, type hints work (unlike with [PyMongo](https://pymongo.readthedocs.io/en/stable/) or [Motor](https://motor.readthedocs.io/en/stable/)), and it's cool. After `Storage` is bound to Motor client using `pymotyc.Engine()`, it can be freely used anytime as long as Mongo is up.

`backend.settings` is straightforward, it simply loads environment variables (that were added to the environment from `.env`) once and stores them. Not always very convenient because if you change the ENV variable value at runtime, you'll have to restart the container, but it won't be that big of a problem anyway (solved with a couple lines of code).

Also, I decided to use `fastapi_utils` just for `StrEnum` because for me as an API user, having descriptive names looked much better than having some number values. There are some workarounds of course, but this to me is the simplest way.

### Mongo is evil, and I hate `ObjectId`

Since `Pydantic` cannot validate `bson.ObjectId` type, models containing `id` field of that type will crash the app, and so will `FastAPI` if by accident you use `ObjectId` as parameter or method return type.

`Pymotyc` offers a workaround that can be seen in `backend.models.weapon`.

To avoid crashes but preserve the ID magic, you have to create 3 models:
1. Input model that has all the base fields. It can only come from API users.
2. Normal model. It has MongoDB's `ObjectId` field. Only this model is stored in the database, and only this model is used within API.
3. Output model that has `id` field of type `str`. This model can only be created from normal model, and should only go back to API user.

Conversion between models is very simple (seen in the same file in normal and out models), but of course it consumes computational resources.

So that's why I liked email keys instead of IDs, hehe. (Refer to `backend.models.player` and respective collection in `backend.storage`).