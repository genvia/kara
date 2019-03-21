# -*- coding: robot -*-

| *** Settings *** |
| Default Tags     | 卡密下单                                                |
| Metadata         | Version                                                 | 0.01              |
| Metadata         | Author                                                  | pangdinghai       |
| Metadata         | Running Id                                              | ${KARA_CLIENT_ID} |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}common.robot   |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}dbutils.robot  |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}opa.robot      |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}ofrg.robot     |
| Variables        | %{KARA_HOME}${/}features${/}variables${/}opa_special.py |

*** Variables *** 
| &{NORMAL_CARDID}    | cardid=1227400 |
| &{NOT_STOCK_CARDID} | cardid=2107501 |
| &{REPEAT_ORDERS}    | cardid=1227400 | sporder_id=${KARA_CLIENT_ID} | userid=A10000009 |
| &{WILL_FAILURE_ID}  | cardid=2137601        |
| ${PUBLIC_WAREHOUSE} | S004134        |
| &{WRONG_PASSWORD}   | card_passwd=XXX  |

| *** Test Cases *** |
| 卡密商品下单成功   |
|                    | ${opa}=                     | 大接口标准版本下单            | CARD_PASS                            | ${True}                    | ${NORMAL_CARDID}        |
|                    | ${verify_result}=           | 验证大接口标准版本下单响应    | ${opa.resp_text}                     | //retcode                  | 1                       | //sporder_id          | ${opa.oflinkid}    | //orderid | ${opa.billid} |
|                    | Should Be True              | ${verify_result}              |
|                    | Comment                     | 校验销售订单                  |
|                    | ${where_cond}=              | create list                   | oflinkid=${opa.oflinkid}             | usercode=${opa.userid}     |
|                    | ${rec}=                     | 数据库查询                    | main@SALEBILLTABLE                   | ${where_cond}              |
|                    | Batch Should Be Equal       | ${rec.billstat}               | ${billstate_payed}                   | ${rec.billid}              | ${opa.billid}           | ${rec.already}        | ${already_success} |
|                    | Comment                     | 校验系统订单                  |
|                    | ${where_cond}=              | create list                   | sale_order_id=${opa.billid}          |
|                    | ${rec_system}=              | 数据库查询                    | ofrcmain@TB_SYSTEM_CARD_PASS_ORDER   | ${where_cond}              |
|                    | Batch Should Be Equal       | ${rec_system.sale_order_id}   | ${opa.billid}                        | ${rec_system.of_link_id}   | ${opa.oflinkid}         | ${rec_system.state}   | ${ofrg_state_16}   |
|                    | Batch Should Be Equal       | ${rec_system.email}           | ${opa.payload["email"]}              | ${rec_system.mobile_no}    | ${opa.payload["phone"]} |
|                    | Batch Should Be Equal       | ${rec_system.card_id}         | ${opa.payload["cardid"]}             |
|                    | Should Be Equal As Integers | ${rec_system.num}             | ${opa.payload["cardnum"]}            |
|                    | Comment                     | 校验充值订单                  |
|                    | ${where_cond}=              | create list                   | sys_order_id=${rec_system.order_id}  |
|                    | ${rec_count}=               | 数据库中记录条数              | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}              |
|                    | Should Be Equal As Integers | ${rec_count}                  | ${1}                                 |
|                    | ${rec_recharge}=            | 数据库查询                    | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}              |
|                    | Batch Should Be Equal       | ${rec_recharge.sale_order_id} | ${opa.billid}                        | ${rec_recharge.of_link_id} | ${opa.oflinkid}         | ${rec_recharge.state} | ${ofrg_state_16}   |
|                    | Batch Should Be Equal       | ${rec_recharge.email}         | ${opa.payload["email"]}              | ${rec_recharge.mobile_no}  | ${opa.payload["phone"]} |
|                    | Batch Should Be Equal       | ${rec_recharge.card_id}       | ${opa.payload["cardid"]}             |
|                    | Should Be Equal As Integers | ${rec_system.num}             | ${opa.payload["cardnum"]}            |

| 卡密商品下单库存不足 |
|                      | ${opa}=            | 大接口标准版本下单         | CARD_PASS                            | ${False}                  | ${NOT_STOCK_CARDID} |
|                      | ${verify_result}=  | 验证大接口标准版本下单响应 | ${opa.resp_text}                     | //retcode                 | 1004                | //err_msg | 此商品暂不可用 |
|                      | Should Be True     | ${verify_result}           |
|                      | Comment            | 校验销售订单               |
|                      | ${where_cond}=     | create list                | oflinkid=${opa.oflinkid}             | usercode=${opa.userid}    |
|                      | ${is_exist}=       | 数据库中记录是否存在       | main@salebilltable                   | ${where_cond}             |
|                      | Should Not Be True | ${is_exist}                |
|                      | Comment            | 校验充值订单               |
|                      | ${where_cond}=     | create list                | of_link_id=${opa.oflinkid}           | merchant_no=${opa.userid} |
|                      | ${is_exist}=       | 数据库中记录是否存在       | ofrcmain@TB_SYSTEM_CARD_PASS_ORDER   | ${where_cond}             |
|                      | Should Not Be True | ${is_exist}                |
|                      | ${where_cond}=     | create list                | of_link_id=${opa.oflinkid}           | merchant_no=${opa.userid} |
|                      | ${is_exist}=       | 数据库中记录是否存在       | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}             |
|                      | Should Not Be True | ${is_exist}                |

| 卡密商品提卡失败 |
|                  | [Setup]                     | 将卡密密码改为错误的          | ${WILL_FAILURE_ID['cardid']}         |
|                  | ${opa}=                     | 大接口标准版本下单            | CARD_PASS                            | ${True}                    | ${WILL_FAILURE_ID}      |
|                  | ${verify_result}=           | 验证大接口标准版本下单响应    | ${opa.resp_text}                     | //retcode                  | 1                       | //sporder_id          | ${opa.oflinkid}     | //orderid | ${opa.billid} |
|                  | Should Be True              | ${verify_result}              |
|                  | Comment                     | 校验销售订单                  |
|                  | ${where_cond}=              | create list                   | oflinkid=${opa.oflinkid}             | usercode=${opa.userid}     |
|                  | ${rec}=                     | 数据库查询                    | main@SALEBILLTABLE                   | ${where_cond}              |
|                  | Batch Should Be Equal       | ${rec.billstat}               | ${billstate_payed}                   | ${rec.billid}              | ${opa.billid}           | ${rec.already}        | ${already_underway} |
|                  | Comment                     | 校验系统订单                  |
|                  | ${where_cond}=              | create list                   | sale_order_id=${opa.billid}          |
|                  | ${rec_system}=              | 数据库查询                    | ofrcmain@TB_SYSTEM_CARD_PASS_ORDER   | ${where_cond}              |
|                  | Batch Should Be Equal       | ${rec_system.sale_order_id}   | ${opa.billid}                        | ${rec_system.of_link_id}   | ${opa.oflinkid}         | ${rec_system.state}   | ${ofrg_state_13}    |
|                  | Batch Should Be Equal       | ${rec_system.email}           | ${opa.payload["email"]}              | ${rec_system.mobile_no}    | ${opa.payload["phone"]} |
|                  | Batch Should Be Equal       | ${rec_system.card_id}         | ${opa.payload["cardid"]}             |
|                  | Should Be Equal As Integers | ${rec_system.num}             | ${opa.payload["cardnum"]}            |
|                  | Comment                     | 校验充值订单                  |
|                  | ${where_cond}=              | create list                   | sys_order_id=${rec_system.order_id}  |
|                  | ${rec_count}=               | 数据库中记录条数              | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}              |
|                  | Should Be Equal As Integers | ${rec_count}                  | ${1}                                 |
|                  | ${rec_recharge}=            | 数据库查询                    | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}              |
|                  | Batch Should Be Equal       | ${rec_recharge.sale_order_id} | ${opa.billid}                        | ${rec_recharge.of_link_id} | ${opa.oflinkid}         | ${rec_recharge.state} | ${ofrg_state_13}    |
|                  | Batch Should Be Equal       | ${rec_recharge.email}         | ${opa.payload["email"]}              | ${rec_recharge.mobile_no}  | ${opa.payload["phone"]} |
|                  | Batch Should Be Equal       | ${rec_recharge.card_id}       | ${opa.payload["cardid"]}             |
|                  | Should Be Equal As Integers | ${rec_system.num}             | ${opa.payload["cardnum"]}            |
| 卡密商品重复下单 |
|                  | ${opa}=                     | 大接口标准版本下单            | CARD_PASS                            | ${True}                    | ${REPEAT_ORDERS}        |
|                  | ${verify_result}=           | 验证大接口标准版本下单响应    | ${opa.resp_text}                     | //retcode                  | 1                       | //sporder_id          | ${opa.oflinkid}     | //orderid | ${opa.billid} |
|                  | Should Be True              | ${verify_result}              |
|                  | Comment                     | 校验销售订单                  |
|                  | ${where_cond}=              | create list                   | oflinkid=${opa.oflinkid}             | usercode=${opa.userid}     |
|                  | ${rec}=                     | 数据库查询                    | main@SALEBILLTABLE                   | ${where_cond}              |
|                  | Batch Should Be Equal       | ${rec.billstat}               | ${billstate_payed}                   | ${rec.billid}              | ${opa.billid}           | ${rec.already}        | ${already_success}  |
|                  | Comment                     | 校验系统订单                  |
|                  | ${where_cond}=              | create list                   | sale_order_id=${opa.billid}          |
|                  | ${rec_system}=              | 数据库查询                    | ofrcmain@TB_SYSTEM_CARD_PASS_ORDER   | ${where_cond}              |
|                  | Batch Should Be Equal       | ${rec_system.sale_order_id}   | ${opa.billid}                        | ${rec_system.of_link_id}   | ${opa.oflinkid}         | ${rec_system.state}   | ${ofrg_state_16}    |
|                  | Batch Should Be Equal       | ${rec_system.email}           | ${opa.payload["email"]}              | ${rec_system.mobile_no}    | ${opa.payload["phone"]} |
|                  | Batch Should Be Equal       | ${rec_system.card_id}         | ${opa.payload["cardid"]}             |
|                  | Should Be Equal As Integers | ${rec_system.num}             | ${opa.payload["cardnum"]}            |
|                  | Comment                     | 校验充值订单                  |
|                  | ${where_cond}=              | create list                   | sys_order_id=${rec_system.order_id}  |
|                  | ${rec_count}=               | 数据库中记录条数              | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}              |
|                  | Should Be Equal As Integers | ${rec_count}                  | ${1}                                 |
|                  | ${rec_recharge}=            | 数据库查询                    | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}              |
|                  | Batch Should Be Equal       | ${rec_recharge.sale_order_id} | ${opa.billid}                        | ${rec_recharge.of_link_id} | ${opa.oflinkid}         | ${rec_recharge.state} | ${ofrg_state_16}    |
|                  | Batch Should Be Equal       | ${rec_recharge.email}         | ${opa.payload["email"]}              | ${rec_recharge.mobile_no}  | ${opa.payload["phone"]} |
|                  | Batch Should Be Equal       | ${rec_recharge.card_id}       | ${opa.payload["cardid"]}             |
|                  | Should Be Equal As Integers | ${rec_system.num}             | ${opa.payload["cardnum"]}            |
|                  | Comment                     | 校验重复下单                  |
|                  | ${opa}=                     | 大接口标准版本下单            | CARD_PASS                            | ${True}                    | ${REPEAT_ORDERS}        |
|                  | ${verify_result}=           | 验证大接口标准版本下单响应    | ${opa.resp_text}                     | //retcode                  | 1                       | //sporder_id          | ${opa.oflinkid}     | //orderid | ${opa.billid} |
|                  | Should Be True              | ${verify_result}              |
|                  | ${where_cond}=              | create list                   | oflinkid=${opa.oflinkid}             | usercode=${opa.userid}     |
|                  | ${rec_count}=               | 数据库中记录条数              | main@Salebilltable                   | ${where_cond}              |
|                  | Should Be Equal As Integers | ${rec_count}                  | ${1}                                 |
|                  | ${where_cond}=              | create list                   | sale_order_id=${opa.billid}          |
|                  | ${rec_count}=               | 数据库中记录条数              | ofrcmain@TB_SYSTEM_CARD_PASS_ORDER   | ${where_cond}              |
|                  | Should Be Equal As Integers | ${rec_count}                  | ${1}                                 |
|                  | ${rec_count}=               | 数据库中记录条数              | ofrcmain@TB_RECHARGE_CARD_PASS_ORDER | ${where_cond}              |
|                  | Should Be Equal As Integers | ${rec_count}                  | ${1}                                 |

*** Keywords *** 
| 将卡密密码改为错误的 |
|                      | [Arguments]    | ${cardid}   |
|                      | ${where_cond}= | create list | user_id=${PUBLIC_WAREHOUSE} | card_type_id=${cardid} | status=0          |
|                      | ${rec}=        | 数据库更新  | cardbase@tb_cardbase        | ${where_cond}          | ${WRONG_PASSWORD} |

# vim: set ft=robot nowrap ai et nu ts=4 sw=4 tw=240:
