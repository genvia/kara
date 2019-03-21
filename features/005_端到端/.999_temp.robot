*** Settings ***
| Metadata  | Version                                                 | 0.01              |
| Metadata  | Author                                                  | pangdinghai       |
| Metadata  | Running Id                                              | ${KARA_CLIENT_ID} |
| Resource  | %{KARA_HOME}${/}features${/}resources${/}common.robot   |
| Resource  | %{KARA_HOME}${/}features${/}resources${/}dbutils.robot  |
| Resource  | %{KARA_HOME}${/}features${/}resources${/}opa.robot      |
| Resource  | %{KARA_HOME}${/}features${/}resources${/}ofrg.robot     |
| Variables | %{KARA_HOME}${/}features${/}variables${/}opa_special.py |

*** Variables *** 


*** Test Cases *** 
| 下话费快充订单并回调撤销 |
|                          | [Setup]               | 数据库执行SQL文件          | ofrc                     | clean_ofrg_orders.sql    |
|                          | ${opa}=               | 大接口标准版本下单         | HF_KC                    |
|                          | ${verify_result}=     | 验证大接口标准版本下单响应 | ${opa.resp_text}         | //retcode                | 1                  | //sporder_id     | ${opa.oflinkid}    |
|                          | Should Be True        | ${verify_result}           |
|                          | ${where_cond}=        | create list                | oflinkid=${opa.oflinkid} | userid=${opa.userid}     |
|                          | ${rec}=               | 数据库查询                 | main@salebilltable       | ${where_cond}            |
|                          | Batch Should Be Equal | ${rec.billstat}            | ${billstate_payed}       | ${rec.billid}            | ${opa.billid}      | ${rec.gamecount} | ${opa.game_userid} |
|                          | ${rec}=               | 数据库查询                 | ofrc@t_sys_orders        | outorderid=${opa.billid} |
|                          | Batch Should Be Equal | ${rec.add_m_no}            | ${opa.userid}            | ${rec.state}             | ${ofrg_state_11}   | ${rec.ordertype} | HF                 |
|                          | ${curr_supuid}=       | Sub Element From String    | ${rec.support_supuids}   |
|                          | ${fetch}=             | 供货商取单                 | ${curr_supuid}           |
|                          | ${rec}=               | 数据库查询                 | ofrc@t_sys_orders        | outorderid=${opa.billid} |
|                          | Batch Should Be Equal | ${rec.supuid}              | ${curr_supuid}           | ${rec.state}             | ${ofrg_state_12}   |
|                          | ${callback}=          | 供货商回调撤销             | ${curr_supuid}           | ${opa.billid}            |
|                          | ${rec}=               | 数据库查询                 | ofrc@t_sys_orders        | outorderid=${opa.billid} |
|                          | Batch Should Be Equal | ${rec.state}               | ${ofrg_state_15}         |
|                          | ${rec}=               | 数据库查询                 | main@salebilltable       | billid=${opa.billid}     |
|                          | Batch Should Be Equal | ${rec.already}             | ${already_cancel}        | ${rec.completestatus}    | ${complete_cancel} |
|                          | log                   | ${OPA_PARAMS_USER_LIMITED} |

| 下话费快充订单并回调成功 |
|                          | [Setup]               | 数据库执行SQL文件          | ofrc                     | clean_ofrg_orders.sql    | state=15
|                          | ${opa}=               | 大接口标准版本下单         | HF_KC                    |
|                          | ${verify_result}=     | 验证大接口标准版本下单响应 | ${opa.resp_text}         | //retcode                | 1                   | //sporder_id     | ${opa.oflinkid}    |
|                          | Should Be True        | ${verify_result}           |
|                          | ${where_cond}=        | create list                | oflinkid=${opa.oflinkid} | userid=${opa.userid}     |
|                          | ${rec}=               | 数据库查询                 | main@salebilltable       | ${where_cond}            |
|                          | Batch Should Be Equal | ${rec.billstat}            | ${billstate_payed}       | ${rec.billid}            | ${opa.billid}       | ${rec.gamecount} | ${opa.game_userid} |
|                          | ${rec}=               | 数据库查询                 | ofrc@t_sys_orders        | outorderid=${opa.billid} |
|                          | Batch Should Be Equal | ${rec.add_m_no}            | ${opa.userid}            | ${rec.state}             | ${ofrg_state_11}    | ${rec.ordertype} | HF                 |
|                          | ${curr_supuid}=       | Sub Element From String    | ${rec.support_supuids}   |
|                          | ${fetch}=             | 供货商取单                 | ${curr_supuid}           |
|                          | ${rec}=               | 数据库查询                 | ofrc@t_sys_orders        | outorderid=${opa.billid} |
|                          | Batch Should Be Equal | ${rec.supuid}              | ${curr_supuid}           | ${rec.state}             | ${ofrg_state_12}    |
|                          | ${callback}=          | 供货商回调成功             | ${curr_supuid}           | ${opa.billid}            |
|                          | ${rec}=               | 数据库查询                 | ofrc@t_sys_orders        | outorderid=${opa.billid} |
|                          | Batch Should Be Equal | ${rec.state}               | ${ofrg_state_16}         |
|                          | ${rec}=               | 数据库查询                 | main@salebilltable       | billid=${opa.billid}     |
|                          | Batch Should Be Equal | ${rec.already}             | ${already_success}       | ${rec.completestatus}    | ${complete_success} |

# vim: set ft=robot ai et nu ts=4 sw=4 tw=240:
