from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from time import sleep
from slackers.server import router

from gptapi import get_answer
from key_word_search import get_sentences

# set permitted cors origins
origins = [
    "*"
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router, prefix="/slack")

def ask_question(q: str):
    print(q)
    # TODO: Get keywords from request_body.query (The question) using stop words dict
    # TODO: Look for relevant paragraphs in paragraphs array
    # TODO: Send request with appropriate token size (10000?) to gpt-3 to get an answer

    lst = get_lst()

    answer = False

    if not answer:
        paragraphs = get_sentences(q)

        for i in paragraphs:
            print(i)
            print('')
            print('')

        answer = get_answer(q, paragraphs)

        print("Answer generated by GPT-3:")
        print(answer)

        # set alarm
        signal.alarm(TIMEOUT)
        send = sleep_input("Send generated answer?")
        # disable the alarm after success
        signal.alarm(0)

        if send != "y" and send is not None:
            print(send)
            print("Answer not sent.")
            answer = "I do not know the answer to this question."


    return answer

import slack


@app.on_event("startup")
async def startup():
    # TODO: populate database/preprocess text files
    print("app started")


@app.on_event("shutdown")
async def shutdown():
    print("app stopped")


# see here: https://fastapi.tiangolo.com/advanced/response-directly/

test_paragraphs = [
    "All Siemens employees are prohibited from offering, promising or making facilitation payments . No such authorization will be granted. The same applies to payments or the granting of other benefits of comparable characteristics and with a comparable purpose to private commercial counterparties.",
    "This prohibition may not be circumvented by making facilitation payments indirectly through third parties . When working with third parties, employees must therefore look out for any indications, for example on invoices, that such third parties may have made or may be making facilitation payments in the context of their activities for Siemens.",
    "In many jurisdictions, a payment under duress is not deemed an act of corruption. In other countries, a situation of duress is at least recognized as justification or as grounds for exemption from punishment. Correspondingly, no Siemens employees are expected to risk life, limb or liberty in the course of performing their duties. Unjustified payments under duress will therefore not be punished with disciplinary action under the following conditions: Any employee should ask the person demanding the payment to explain the legal basis for the demand and inquire whether an official account or receipt will be issued for the payment . If it becomes evident that the payment demanded most likely constitutes a facilitation payment, either because there is no plausible legal basis for such payment or because the government official refuses to issue an official invoice or receipt, the employee should oppose the demand as strongly as possible. If a situation of duress arises, it is permissible to yield to the request to make a facilitation payment. Expenditure in connection with facilitation payments is generally not reimbursed to employees or third parties acting for Siemens . Provided that the employee has complied in full with the applicable reporting and documentation obligations and there are no specific circumstances indicating that the employee is at fault in connection with the payment, disciplinary action will generally be disproportionate because the employee will have allowed Siemens to meet its statutory documentation duties."
]

import signal

TIMEOUT = 2  # number of seconds your want for timeout


def interrupted():
    print('interrupted!')


signal.signal(signal.SIGALRM, interrupted)


def sleep_input(q):
    try:
        foo = input(q)
        return foo
    except:
        # timeout
        return


@app.get("/api/question")
async def question(q: str):
    return JSONResponse(content=ask_question(q))

