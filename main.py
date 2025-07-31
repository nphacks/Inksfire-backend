from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from models.tags import TagsSearchQuery
from routes.project_setup import router as project_setup_router
from routes.project import router as project_router
from routes.story import router as story_router
from routes.qloo import router as qloo_router, movie_information_search, actor_information_search
from routes.llm import router as llm_generate_router, suggest_tags, generate_ideas
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:4200"], 
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "genai-key.json"


app.include_router(project_setup_router, prefix="/project-setup")
app.include_router(project_router, prefix="/project")
app.include_router(story_router, prefix="/story")
app.include_router(llm_generate_router, prefix="/llm")
app.include_router(qloo_router, prefix="/qloo")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
async def root():
    # REMOVE THIS
    # test_input = TagsSearchQuery(
    #     searchString='adventure',
    #     idea='A window woman begins to live her childhood dream of riding motorbike.',
    #     genres='adventure, comedy',
    #     story_types='movie',
    #     target_age='24_and_younger, 25_to_29',
    #     target_gender='{"male":0.5,"female":0.5}'
    # )
    # await suggest_tags(test_input)

    # Test call to suggest_tags
    # await generate_ideas()  # make sure suggest_tags is async 

    # await movie_information_search('movies about space')
    # await actor_information_search('korean actors above 25 and who can sing')
    return {"status_code": 200, "message": "Connected to Backend!"}