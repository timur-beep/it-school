import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import back.routes as rts

origins = ["http://localhost:3000", "http://localhost:3002"]

app = FastAPI(
    title="IT Camp Тестовое Приложение",
    description="Обучающее приложение по созданию простых API",
    license_info={
        "name": "The Unlicense",
        "url": "https://unlicense.org",
    },
)

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])

app.include_router(rts.main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
