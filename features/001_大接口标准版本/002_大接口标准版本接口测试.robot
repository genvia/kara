| *** Settings *** |
| Default Tags   | 大接口标准版本 |
| Metadata       | Version | 0.01 |
| Metadata       | Author | jinmaochen |
| Metadata       | Running Id | ${KARA_CLIENT_ID} |
| Resource       | %{KARA_HOME}${/}features${/}resources${/}common.robot |
| Resource       | %{KARA_HOME}${/}features${/}resources${/}dbutils.robot |
| Resource       | %{KARA_HOME}${/}features${/}resources${/}opa.robot |
| Variables      | %{KARA_HOME}${/}features${/}variables${/}opa_special.py |

| *** Test Cases *** |
| 大接口标准版本话费类目的商品下单 |
|    | 大接口标准版本类目下单和校验 | HF_KC |

| *** Keywords *** |
| 大接口标准版本类目下单和校验 |
|    | [Arguments] | ${order_type} | ${sporder_id}=sporder_id |
|    | [Documentation] | 大接口标准版本下单，参数是订单的类型，例如HF LL CARD_PASS之类，并针对返回信息和数据信息录入进行校验 |
|    | ${opa}= | 大接口标准版本下单 | ${order_type} |
|    | ${verify_result} | run keyword if | '${order_type}'=='JINRONG' | 验证大接口标准版本下单响应 | ${opa.resp_text} | //retcode | 1 |
|    | ... | ELSE | 验证大接口标准版本下单响应 | ${opa.resp_text} | //retcode | 1 | //${sporder_id} |
|    | ... | ${opa.oflinkid} |
|    | Should Be True | ${verify_result} |
|    | Simple Delay |
|    | ${where_cond}= | create list | oflinkid=${opa.oflinkid} | usercode=${opa.userid} |
|    | ${rec}= | 数据库查询 | main@salebilltable | ${where_cond} |
|    | Batch Should Be Equal | ${rec.billstat} | ${billstate_payed} | ${rec.billid} | ${opa.billid} | ${rec.gamecount} | ${opa.game_userid} |
