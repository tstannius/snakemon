#!/bin/bash

export SECRET_KEY="7ef03134ec21e6bc77a138553e56112554940b827e37bfedfa2aec5c12a637b3"

uvicorn app.main:app --reload
