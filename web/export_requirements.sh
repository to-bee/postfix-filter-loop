#!/bin/bash

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
pip freeze > requirements.txt