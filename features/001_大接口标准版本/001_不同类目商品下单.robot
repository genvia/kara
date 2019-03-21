*** Settings ***
Default Tags      大接口标准版本
Metadata          Version    0.01
Metadata          Author    pangdinghai
Metadata          Running Id    ${KARA_CLIENT_ID}
Resource          %{KARA_HOME}${/}features${/}resources${/}common.robot
Resource          %{KARA_HOME}${/}features${/}resources${/}dbutils.robot
Resource          %{KARA_HOME}${/}features${/}resources${/}opa.robot
Variables         %{KARA_HOME}${/}features${/}variables${/}opa_special.py

*** Variables ***
@{all_category}    流量    \| 话费快充 \| 游戏 \| 加油卡

*** Test Cases ***
大接口标准版本使用主要类目的商品下单
    [Template]    大接口标准版本使用${category}商品下单
    : FOR    ${category}    IN    @{all_category}
    \    ${category}

大接口标准版本话费类目的商品下单
    大接口标准版本类目下单和校验    HF_KC

大接口标准版本流量类目的商品下单
    大接口标准版本类目下单和校验    LL

大接口标准版本加油卡类目的商品下单
    大接口标准版本类目下单和校验    GAS_CARD

大接口标准版本游戏类目的商品下单
    大接口标准版本类目下单和校验    SUP_GAME

大接口标准版本公共事业类目的商品下单
    大接口标准版本类目下单和校验    GGSHIYE    sporderId

大接口标准版本金融类目的商品下单
    大接口标准版本类目下单和校验    JINRONG

大接口标准版本话费类目固话商品下单
    大接口标准版本类目下单和校验    HF_GH

大接口标准版本话费类目宽带商品下单
    大接口标准版本类目下单和校验    HF_KD

大接口标准版本礼品卡类目商品下单
    大接口标准版本类目下单和校验    GIFT

大接口标准版本公共事业类目缴费卡商品下单
    大接口标准版本类目下单和校验    GGSHIYECARD    sporderId

大接口标准版本话费类目慢充的商品下单
    大接口标准版本类目下单和校验    HF_MC

*** Keywords ***
大接口标准版本使用${category}商品下单
    ${order_type}=    Set Variable If    "${category}" == "话费快充"    HF_KC    "${category}" == "固话宽带"    HF_GH    "${category}" == "流量"
    ...    LL    "${category}" == "游戏"    SUP_GAME    "${category}" == "加油卡"    GAS_CARD    "${category}" == "提取卡密"
    ...    CARD_PASS    "${category}" == "公共事业"    GGSHIYE
    Should Not Be Equal    ${order_type}    ${None}
    ${opa}=    大接口标准版本下单    ${order_type}
    ${verify_result}=    验证大接口标准版本下单响应    ${opa.resp_text}    //retcode    1    //sporder_id    ${opa.oflinkid}
    Should Be True    ${verify_result}
    ${where_cond}=    create list    oflinkid=${opa.oflinkid}    usercode=${opa.userid}
    ${rec}=    数据库查询    main@salebilltable    ${where_cond}
    Batch Should Be Equal    ${rec.billstat}    ${billstate_payed}    ${rec.billid}    ${opa.billid}    ${rec.gamecount}    ${opa.game_userid}

大接口标准版本类目下单和校验
    [Arguments]    ${order_type}    ${sporder_id}=sporder_id
    [Documentation]    大接口标准版本下单，参数是订单的类型，例如HF LL CARD_PASS之类，并针对返回信息和数据信息录入进行校验
    ${opa}=    大接口标准版本下单    ${order_type}
    ${verify_result}    run keyword if    '${order_type}'=='JINRONG'    验证大接口标准版本下单响应    ${opa.resp_text}    //retcode    1
    ...    ELSE    验证大接口标准版本下单响应    ${opa.resp_text}    //retcode    1    //${sporder_id}
    ...    ${opa.oflinkid}
    Should Be True    ${verify_result}
    Simple Delay
    ${where_cond}=    create list    oflinkid=${opa.oflinkid}    usercode=${opa.userid}
    ${rec}=    数据库查询    main@salebilltable    ${where_cond}
    Batch Should Be Equal    ${rec.billstat}    ${billstate_payed}    ${rec.billid}    ${opa.billid}    ${rec.gamecount}    ${opa.game_userid}
