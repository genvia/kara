*** Settings ***
Documentation     帐务相关操作的关键字
...               Author Pangdinghai
...               Version 0.0.1
Library           kararfsclient.KaraLibs
Resource          %{KARA_HOME}${/}features${/}resources${/}common.robot

*** Variables ***

*** Keywords ***
帐务下单
    [Arguments]    ${params_dict}
    [Documentation]    帐务下单
    ${kernel}=    Kernel Make Order    ${params_dict}
    sleep    ${DELAY_TIME}
    [Return]    ${kernel}

帐务回调
    [Arguments]    ${params_dict}
    [Documentation]    帐务下单
    ${kernel}=    Kernel Make Callback    ${params_dict}
    sleep    ${DELAY_TIME}
    [Return]    ${kernel}
