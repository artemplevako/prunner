from enum import Enum
from subprocess import Popen, PIPE
from typing import Annotated, Optional

from fastapi import FastAPI
from fastapi import status, HTTPException
from fastapi import Body
from pydantic import BaseModel, Field


class Action(str, Enum):
    start = 'start'
    stop = 'stop'


class ProcessResult(BaseModel):
    pid: int = Field(
        title='Process ID',
        description='The ID of the completed process',
        example=12
    )
    exit_code: int = Field(
        title='Exit status code',
        description='The exit status code of the completed process',
        example=0
    )
    stdout: str = Field(
        title='Process output',
        description='The output of the completed process',
        example='The process is very useful'
    )
    stderr: str = Field(
        title='Process error output',
        description='The error output of the completed process',
        example='Error: the process has failed'
    )


class ActionResult(BaseModel):
    pid: int = Field(
        title='Process ID',
        description='The ID of a process the action is performed on',
        example=12
    )


tags_metadata = [{'name': 'methods'}]

app = FastAPI(
    title='prunner',
    description='Run an isolated process',
    redoc_url=None,
    openapi_tags=tags_metadata
)

proc_name = 'timer'
proc = None


@app.get(f'/{proc_name}', tags=['methods'])
async def is_running() -> bool:
    return proc is not None and proc.poll() is None


@app.post(
    f'/{proc_name}',
    status_code=status.HTTP_201_CREATED,
    tags=['methods']
)
async def do_action(
    action: Annotated[Action, Body(
        title='Action type',
        description='Action type to perform on process'
    )]
) -> ActionResult:
    global proc
    if action is Action.start:
        if await is_running():
            raise HTTPException(
                status_code=401, detail='The process is already running'
            )
        proc = Popen('./timer', stdout=PIPE, stderr=PIPE)
    elif action is Action.stop:
        if proc is None or not await is_running():
            raise HTTPException(
                status_code=402, detail='There is no running process'
            )
        proc.terminate()
    return ActionResult(pid=proc.pid)


@app.get(f'/{proc_name}/result', tags=['methods'])
async def get_result() -> ProcessResult:
    if proc is None or await is_running():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Not Found'
        )
    return ProcessResult(
        pid=proc.pid,
        exit_code=proc.returncode,
        stdout=proc.stdout.read(),
        stderr=proc.stderr.read()
    )
