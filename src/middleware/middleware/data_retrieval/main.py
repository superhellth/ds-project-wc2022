import elasticsearch
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

INDEX_NAME = "tweets"

# elasticsearch instancing: 9200 standard port
es_client = elasticsearch.Elasticsearch("http://45.13.59.173:9200", basic_auth=("elastic", "sicheristsicher"))

# fastapi instance
app = FastAPI()

# allow access from the following addresses:
origins = [
    "http://localhost:5173/",
    "http://localhost:5173",
    "http://localhost",
    "http://localhost/",
    "http://176.199.208.10/",
    "http://176.199.208.10"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def get_tweets():
    """Test"""
    return {"hello":"nico"}


@app.get("/query/")
async def get_tweets():
    """Returns all tweets from the connected elasticsearch instance"""
    resp = es_client.search(index="tweets", size=50,
                            sort={"created_at": "desc"})
    return resp["hits"]["hits"]