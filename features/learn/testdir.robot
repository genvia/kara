*** Settings ***
Library           String
Library           DateTime
Library           Collections

*** Test Cases ***
test1
    log    hello world
    ${abc}    Create List    a    a    b
    Append To List    ${abc}    a    a
    log    ${abc}
