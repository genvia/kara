# -*- coding: robot -*-

| *** Settings *** |
| Default Tags     | 回调                                                    |
| Metadata         | Version                                                 | 0.01                 |
| Metadata         | Author                                                  | pangdinghai          |
| Metadata         | Running Id                                              | ${KARA_CLIENT_ID}    |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}common.robot   |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}dbutils.robot  |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}opa.robot      |
| Resource         | %{KARA_HOME}${/}features${/}resources${/}ofrg.robot     |
| Variables        | %{KARA_HOME}${/}features${/}variables${/}opa_special.py |
| Suite Setup      | 重置订单表中数据的状态                                  | TB_SYSTEM_FLOW_ORDER | TB_RECHARGE_FLOW_ORDER | 50 |

*** Variables *** 
| &{EXTRA_PARMS}   | phoneno=18909160000 | userid=A10000008 | perValue=30 | flowValue=500M |
| ${ORDER_CATGORY} | LL                  |
| ${FIRST_SUPUID}  | 310                 |
| ${SECOND_SUPUID} | 317                 |


| *** Test Cases *** |
| 供货商回调成功     |
|                    | [Setup]                     | 流量商品下单          |
|                    | 供货商取单                  | ${FIRST_SUPUID}       | 1                                   |
|                    | 供货商回调成功              | ${FIRST_SUPUID}       | ${opaobj.billid}                    |
|                    | Comment                     | 校验系统订单          |
|                    | ${where_cond}=              | create list           | sale_order_id=${opaobj.billid}      |
|                    | ${rec_system}=              | 数据库查询            | ofrcmain@TB_SYSTEM_FLOW_ORDER       | ${where_cond} |
|                    | Batch Should Be Equal       | ${rec_system.state}   | ${ofrg_state_16}                    |
|                    | Comment                     | 校验充值订单          |
|                    | ${where_cond}=              | create list           | sys_order_id=${rec_system.order_id} |
|                    | ${rec_count}=               | 数据库中记录条数      | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond} |
|                    | Should Be Equal As Integers | ${rec_count}          | ${1}                                |
|                    | ${rec_recharge}=            | 数据库查询            | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond} |
|                    | Batch Should Be Equal       | ${rec_recharge.state} | ${ofrg_state_16}                    |

| 供货商回调撤销 |
|                | [Setup]                     | 流量商品下单          |
|                | 供货商取单                  | ${FIRST_SUPUID}       | 1                                   |
|                | 供货商回调撤销              | ${FIRST_SUPUID}       | ${opaobj.billid}                    |
|                | Comment                     | 校验系统订单          |
|                | ${where_cond}=              | create list           | sale_order_id=${opaobj.billid}      |
|                | ${rec_system}=              | 数据库查询            | ofrcmain@TB_SYSTEM_FLOW_ORDER       | ${where_cond} |
|                | Batch Should Be Equal       | ${rec_system.state}   | ${ofrg_state_15}                    |
|                | Comment                     | 校验充值订单          |
|                | ${where_cond}=              | create list           | sys_order_id=${rec_system.order_id} |
|                | ${rec_count}=               | 数据库中记录条数      | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond} |
|                | Should Be Equal As Integers | ${rec_count}          | ${1}                                |
|                | ${rec_recharge}=            | 数据库查询            | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond} |
|                | Batch Should Be Equal       | ${rec_recharge.state} | ${ofrg_state_15}                    |

| 供货商回调可疑 |
|                | [Setup]                     | 流量商品下单          |
|                | 供货商取单                  | ${FIRST_SUPUID}       | 1                                   |
|                | 供货商回调可疑              | ${FIRST_SUPUID}       | ${opaobj.billid}                    |
|                | Comment                     | 校验系统订单          |
|                | ${where_cond}=              | create list           | sale_order_id=${opaobj.billid}      |
|                | ${rec_system}=              | 数据库查询            | ofrcmain@TB_SYSTEM_FLOW_ORDER       | ${where_cond} |
|                | Batch Should Be Equal       | ${rec_system.state}   | ${ofrg_state_13}                    |
|                | Comment                     | 校验充值订单          |
|                | ${where_cond}=              | create list           | sys_order_id=${rec_system.order_id} |
|                | ${rec_count}=               | 数据库中记录条数      | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond} |
|                | Should Be Equal As Integers | ${rec_count}          | ${1}                                |
|                | ${rec_recharge}=            | 数据库查询            | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond} |
|                | Batch Should Be Equal       | ${rec_recharge.state} | ${ofrg_state_13}                    |

| 供货商回调失败 |
|                | [Setup]                     | 流量商品下单                    |
|                | 供货商取单                  | ${FIRST_SUPUID}                 | 1                                       |
|                | 供货商回调失败              | ${FIRST_SUPUID}                 | ${opaobj.billid}                        |
|                | Comment                     | 校验系统订单                    |
|                | ${where_cond}=              | create list                     | sale_order_id=${opaobj.billid}          |
|                | ${rec_system}=              | 数据库查询                      | ofrcmain@TB_SYSTEM_FLOW_ORDER           | ${where_cond}               |
|                | Batch Should Be Equal       | ${rec_system.state}             | ${ofrg_state_11}                        | ${rec_system.supplier_id}   | ${SECOND_SUPUID} |
|                | Batch Should Be Equal       | ${rec_system.used_supplier_ids} | ${FIRST_SUPUID},${SECOND_SUPUID}        |
|                | Comment                     | 校验充值订单                    |
|                | ${where_cond}=              | create list                     | sys_order_id=${rec_system.order_id}     |
|                | ${rec_count}=               | 数据库中记录条数                | ofrcmain@TB_RECHARGE_FLOW_ORDER         | ${where_cond}               |
|                | Should Be Equal As Integers | ${rec_count}                    | ${2}                                    |
|                | ${where_cond}=              | create list                     | order_id=${prev_curr_charge_orderid}    |
|                | ${rec_recharge}=            | 数据库查询                      | ofrcmain@TB_RECHARGE_FLOW_ORDER         | ${where_cond}               |
|                | Batch Should Be Equal       | ${rec_recharge.state}           | ${ofrg_state_14}                        | ${rec_recharge.supplier_id} | ${FIRST_SUPUID}  |
|                | ${where_cond}=              | create list                     | order_id=${rec_system.curr_recharge_id} |
|                | ${rec_recharge}=            | 数据库查询                      | ofrcmain@TB_RECHARGE_FLOW_ORDER         | ${where_cond}               |
|                | Batch Should Be Equal       | ${rec_recharge.state}           | ${ofrg_state_11}                        | ${rec_recharge.supplier_id} | ${SECOND_SUPUID} |

*** Keywords *** 
| 流量商品下单 |
|              | ${opa}=                     | 大接口标准版本下单            | ${ORDER_CATGORY}                    | ${True}                    | ${EXTRA_PARMS}  |
|              | ${verify_result}=           | 验证大接口标准版本下单响应    | ${opa.resp_text}                    | //retcode                  | 1               | //sporder_id          | ${opa.oflinkid}  | //orderid | ${opa.billid} |
|              | Should Be True              | ${verify_result}              |
|              | Comment                     | 校验销售订单                  |
|              | ${where_cond}=              | create list                   | oflinkid=${opa.oflinkid}            | usercode=${opa.userid}     |
|              | ${rec}=                     | 数据库查询                    | main@SALEBILLTABLE                  | ${where_cond}              |
|              | Batch Should Be Equal       | ${rec.billstat}               | ${billstate_payed}                  | ${rec.billid}              | ${opa.billid}   |
|              | Comment                     | 校验系统订单                  |
|              | ${where_cond}=              | create list                   | sale_order_id=${opa.billid}         |
|              | ${rec_system}=              | 数据库查询                    | ofrcmain@TB_SYSTEM_FLOW_ORDER       | ${where_cond}              |
|              | Batch Should Be Equal       | ${rec_system.sale_order_id}   | ${opa.billid}                       | ${rec_system.of_link_id}   | ${opa.oflinkid} | ${rec_system.state}   | ${ofrg_state_11} |
|              | Set Test Variable           | ${prev_curr_charge_orderid}   | ${rec_system.curr_recharge_id}      |
|              | Comment                     | 校验充值订单                  |
|              | ${where_cond}=              | create list                   | sys_order_id=${rec_system.order_id} |
|              | ${rec_count}=               | 数据库中记录条数              | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond}              |
|              | Should Be Equal As Integers | ${rec_count}                  | ${1}                                |
|              | ${rec_recharge}=            | 数据库查询                    | ofrcmain@TB_RECHARGE_FLOW_ORDER     | ${where_cond}              |
|              | Batch Should Be Equal       | ${rec_recharge.sale_order_id} | ${opa.billid}                       | ${rec_recharge.of_link_id} | ${opa.oflinkid} | ${rec_recharge.state} | ${ofrg_state_11} |
|              | Set Test Variable           | ${opaobj}                     | ${opa}                              |

# vim: set ft=robot nowrap ai et nu ts=4 sw=4 tw=240:
