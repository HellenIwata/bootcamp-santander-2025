from fastapi import FastAPI

from workout_api.routers import api_router

app = FastAPI(title="Workout API", version="1.0.0")

app.include_router(api_router)

""" if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, log_level="info")
    '''
        "main:app" refers to the 'app' instance in the 'main.py' file.
        "reload" enables auto-reloading on code changes.
        "log_level" sets the logging verbosity.
        "host" and "port" define where the server listens.
    ''' """