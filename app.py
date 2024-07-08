
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import boto3
import os
from mangum import Mangum

app = FastAPI()
dynamo = boto3.client('dynamodb')
table_one_name = os.environ['TABLE_ONE_NAME']
table_two_name = os.environ['TABLE_TWO_NAME']

def respond (err=None, res=None):
    if err:
        raise HTTPException(status_code=400, detail=str(err))
    return JSONResponse(status_code=200, content=res)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the API"}

@app.get("/{table_name}")
async def read_items(table_name: str, request: Request):
    try:
        params = dict(request.query_params)
        table_name = get_table_name(table_name)
        response = dynamo.scan(TableName=table_name, **params) if params else dynamo.scan(TableName=table_name)
        return respond(res=response)
    except Exception as e:
        return respond(err=e)

@app.post("/{table_name}")
async def create_item(table_name: str, request: Request):
    try:
        payload = await request.json()
        table_name = get_table_name(table_name)
        response = dynamo.put_item(TableName=table_name, **payload)
        return respond(res=response)
    except Exception as e:
        return respond(err=e)

@app.put("/{table_name}")
async def update_item(table_name: str, request: Request):
    try:
        payload = await request.json()
        table_name = get_table_name(table_name)
        response = dynamo.update_item(TableName=table_name, **payload)
        return respond(res=response)
    except Exception as e:
        return respond(err=e)

@app.delete("/{table_name}")
async def delete_item(table_name: str, request: Request):
    try:
        payload = await request.json()
        table_name = get_table_name(table_name)
        response = dynamo.delete_item(TableName=table_name, **payload)
        return respond(res=response)
    except Exception as e:
        return respond(err=e)

def get_table_name(table_name_alias: str) -> str:
    if table_name_alias == "table1":
        return table_one_name
    elif table_name_alias == "table2":
        return table_two_name
    else:
        raise HTTPException(status_code=400, detail="Invalid table name")

handler = Mangum(app)
