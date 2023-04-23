from enum import Enum
from subprocess import Popen, PIPE
from typing import Annotated, Optional

from fastapi import FastAPI, status
from fastapi import Body
from pydantic import BaseModel


class Action(str, Enum):
    start = 'start'
    stop = 'stop'


class ProcessResult(BaseModel):
    pid: int
    exit_code: Optional[int]
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
        proc = Popen('./timer', stdout=PIPE, stderr=PIPE)
    elif action is Action.stop:
        proc.kill()
    return proc.pid


@app.get(f'/{proc_name}/result')
async def get_result() -> ProcessResult:
    return ProcessResult(
        pid=proc.pid,
        exit_code=proc.returncode,
        stdout=proc.stdout.read(),
        stderr=proc.stderr.read()
    )
