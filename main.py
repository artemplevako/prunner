from enum import Enum
from subprocess import Popen, PIPE
from typing import Annotated, Optional

from fastapi import FastAPI
from fastapi import status, HTTPException
from fastapi import Body
from pydantic import BaseModel


class Action(str, Enum):
    start = 'start'
    stop = 'stop'


class ProcessResult(BaseModel):
    pid: int
    exit_code: int
    stdout: str
    stderr: str


app = FastAPI()

proc_name = 'timer'
proc = None


@app.get(f'/{proc_name}')
async def is_running() -> bool:
    return proc is not None and proc.poll() is None


@app.post(f'/{proc_name}', status_code=status.HTTP_201_CREATED)
async def do_action(action: Annotated[Action, Body()]) -> int:
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
        proc.kill()
    return proc.pid


@app.get(f'/{proc_name}/result')
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
