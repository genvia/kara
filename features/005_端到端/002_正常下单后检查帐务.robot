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
| ${HFKC_CATE_ID}     | 10401 |
| ${ACCOUNT_TYPE_XYD} | 01    |
| ${ACCOUNT_TYPE_HFF} | 02    |
| ${OCCUR_TYPE_XF}    | 1     |
| ${OCCUR_TYPE_TK}    | 5     |
| ${PAYMENT_TYPE_OUT} | 1     |
| ${PAYMENT_TYPE_IN}  | 0     |

*** Test Cases *** 
| 仅有信用点帐号余额充足的商户下单 |
|                                  | [Setup]                     | 校验用户的帐务信息            | ${OPA_PARAMS_USER_ONLY_XYD_ENGOUGH['userid']}   |
|                                  | Set Test Variable           | ${user_code}                  | ${OPA_PARAMS_USER_ONLY_XYD_ENGOUGH['userid']}   |
|                                  | ${account_xyd}=             | 数据库查询                    | pay@tb_kernel_account                           | user_code=${user_code}              |
|                                  | Comment                     | 数据库查询返回对象            | 如果用obj.propertye形式不出错就表明只有单条数据 | 所以此用户只有信用点                |
|                                  | Should Be Equal             | ${account_xyd.acct_type_id}   | ${ACCOUNT_TYPE_XYD}                             |
|                                  | Should Be Equal As Integers | ${account_xyd.data_status}    | 1                                               |
|                                  | Should Be Equal As Integers | ${account_xyd.lock_status}    | 0                                               |
|                                  | ${old_balance}=             | 获取用户信用点余额            | ${user_code}                                    |
|                                  | log                         | ${old_balance.curr_balance}   |
|                                  | ${opa}=                     | 大接口标准版本自定义参数下单  | onlineorder.do                                  | ${OPA_PARAMS_USER_ONLY_XYD_ENGOUGH} |
|                                  | Set Test Variable           | ${billid}                     | ${opa.billid}                                   |
|                                  | 下单后初步检查              | ${opa}                        | ${user_code}                                    | ${billid}                           |
|                                  | ${pay_order}=               | 数据库查询                    | pay@tb_kernel_pay_order                         | sale_sys_orderid=${billid}          |
|                                  | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.pay_amount}                         |
|                                  | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.order_cash}                         |
|                                  | Should Be Equal As Integers | ${pay_order.pay_status}       | 1                                               |
|                                  | Should Be Equal             | ${pay_order.out_order_id}     | ${opa.oflinkid}                                 |
|                                  | ${new_balance}=             | 获取用户信用点余额            | ${user_code}                                    |
|                                  | log                         | ${new_balance.curr_balance}   |
|                                  | ${balance_diff}=            | Evaluate                      | 1000 * ${salebilltable.cash}                    |
|                                  | ${expect_balance}=          | Evaluate                      | ${new_balance.curr_balance} + ${balance_diff}   |
|                                  | log many                    | ${new_balance.curr_balance}   | ${balance_diff}                                 | ${expect_balance}                   | ${old_balance.curr_balance} |
|                                  | Should Be Equal As Numbers  | ${expect_balance}             | ${old_balance.curr_balance}                     |
|                                  | ${where_cond}=              | create list                   | acct_id=${account_xyd.acct_id}                  | sale_sys_orderid=${billid}          |
|                                  | ${balance_order}=           | 数据库查询                    | pay@tb_kernel_blc_order                         | ${where_cond}                       |
|                                  | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${balance_order.pay_cash}                       |
|                                  | Should Be Equal As Numbers  | ${new_balance.curr_balance}   | ${balance_order.left_balance}                   |
|                                  | Should Be Equal As Integers | ${balance_order.pay_status}   | 1                                               |
|                                  | Should Be Equal As Strings  | ${balance_order.acct_id}      | ${account_xyd.acct_id}                          |
|                                  | Should Be Equal As Strings  | ${balance_order.acct_type_id} | ${ACCOUNT_TYPE_XYD}                             |
|                                  | ${where_cond}=              | create list                   | acct_id=${account_xyd.acct_id}                  | sale_sys_orderid=${billid}          |
|                                  | @{balance_detail}=          | 数据库查询多行记录            | pay@tb_kernel_blcdetail                         | ${where_cond}                       |
|                                  | :FOR                        | ${detail}                     | IN                                              | @{balance_detail}                   |
|                                  |                             | ${final_balance}=             | 获取用户信用点余额                              | ${user_code}                        |
|                                  |                             | Run Keyword If                | ${detail.occur_type} == ${OCCUR_TYPE_TK}        | 校验退款余额明细                    | ${salebilltable}            | ${final_balance.curr_balance} | ${detail} | ${ACCOUNT_TYPE_XYD} |
|                                  |                             | Run Keyword If                | ${detail.occur_type} == ${OCCUR_TYPE_XF}        | 校验支付成功余额明细                | ${salebilltable}            | ${final_balance.curr_balance} | ${detail} | ${ACCOUNT_TYPE_XYD} |

| 信用点和后付费帐号都有，信用点余额充足，信用点优先的商户下单 |
|                                                              | [Setup]                     | 校验用户的帐务信息            | ${OPA_PARAMS_USER_ALL_XYD_ENGOUGH_USE_XYD['userid']} |
|                                                              | Set Test Variable           | ${user_code}                  | ${OPA_PARAMS_USER_ALL_XYD_ENGOUGH_USE_XYD['userid']} |
|                                                              | 校验用户拥有两个可用帐号    | ${user_code}                  | ${True}                                              | 
|                                                              | ${old_balance}=             | 获取用户信用点余额            | ${user_code}                                         |
|                                                              | log                         | ${old_balance.curr_balance}   |
|                                                              | ${opa}=                     | 大接口标准版本自定义参数下单  | onlineorder.do                                       | ${OPA_PARAMS_USER_ALL_XYD_ENGOUGH_USE_XYD} |
|                                                              | Set Test Variable           | ${billid}                     | ${opa.billid}                                        |
|                                                              | 下单后初步检查              | ${opa}                        | ${user_code}                                         | ${billid}                                  |
|                                                              | ${pay_order}=               | 数据库查询                    | pay@tb_kernel_pay_order                              | sale_sys_orderid=${billid}                 |
|                                                              | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.pay_amount}                              |
|                                                              | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.order_cash}                              |
|                                                              | Should Be Equal As Integers | ${pay_order.pay_status}       | 1                                                    |
|                                                              | Should Be Equal             | ${pay_order.out_order_id}     | ${opa.oflinkid}                                      |
|                                                              | ${new_balance}=             | 获取用户信用点余额            | ${user_code}                                         |
|                                                              | log                         | ${new_balance.curr_balance}   |
|                                                              | ${balance_diff}=            | Evaluate                      | 1000 * ${salebilltable.cash}                         |
|                                                              | ${expect_balance}=          | Evaluate                      | ${new_balance.curr_balance} + ${balance_diff}        |
|                                                              | log many                    | ${new_balance.curr_balance}   | ${balance_diff}                                      | ${expect_balance}                          | ${old_balance.curr_balance} |
|                                                              | Should Be Equal As Numbers  | ${expect_balance}             | ${old_balance.curr_balance}                          |
|                                                              | ${where_cond}=              | create list                   | acct_id=${account_xyd.acct_id}                       | sale_sys_orderid=${billid}                 |
|                                                              | ${balance_order}=           | 数据库查询                    | pay@tb_kernel_blc_order                              | ${where_cond}                              |
|                                                              | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${balance_order.pay_cash}                            |
|                                                              | Should Be Equal As Numbers  | ${new_balance.curr_balance}   | ${balance_order.left_balance}                        |
|                                                              | Should Be Equal As Integers | ${balance_order.pay_status}   | 1                                                    |
|                                                              | Should Be Equal As Strings  | ${balance_order.acct_id}      | ${account_xyd.acct_id}                               |
|                                                              | Should Be Equal As Strings  | ${balance_order.acct_type_id} | ${ACCOUNT_TYPE_XYD}                                  |
|                                                              | ${where_cond}=              | create list                   | acct_id=${account_xyd.acct_id}                       | sale_sys_orderid=${billid}                 |
|                                                              | @{balance_detail}=          | 数据库查询多行记录            | pay@tb_kernel_blcdetail                              | ${where_cond}                              |
|                                                              | :FOR                        | ${detail}                     | IN                                                   | @{balance_detail}                          |
|                                                              |                             | ${final_balance}=             | 获取用户信用点余额                                   | ${user_code}                               |
|                                                              |                             | Run Keyword If                | ${detail.occur_type} == ${OCCUR_TYPE_TK}             | 校验退款余额明细                           | ${salebilltable}            | ${final_balance.curr_balance} | ${detail} | ${ACCOUNT_TYPE_XYD} |
|                                                              |                             | Run Keyword If                | ${detail.occur_type} == ${OCCUR_TYPE_XF}             | 校验支付成功余额明细                       | ${salebilltable}            | ${final_balance.curr_balance} | ${detail} | ${ACCOUNT_TYPE_XYD} |


| 信用点和后付费帐号都有，但信用点余额不足的商户下单 |
|                                                    | [Setup]                     | 校验用户的帐务信息            | ${OPA_PARAMS_USER_ALL_XYD_IS_ZERO_USE_HFF['userid']} |
|                                                    | Set Test Variable           | ${user_code}                  | ${OPA_PARAMS_USER_ALL_XYD_IS_ZERO_USE_HFF['userid']} |
|                                                    | 校验用户拥有两个可用帐号    | ${user_code}                  | ${True}                                              |
|                                                    | ${old_balance}=             | 获取用户信用点余额            | ${user_code}                                         |
|                                                    | log                         | ${old_balance.curr_balance}   |
|                                                    | Should Be Equal As Numbers  | ${old_balance.curr_balance}   | ${0}
|                                                    | ${opa}=                     | 大接口标准版本自定义参数下单  | onlineorder.do                                       | ${OPA_PARAMS_USER_ALL_XYD_IS_ZERO_USE_HFF} |
|                                                    | Set Test Variable           | ${billid}                     | ${opa.billid}                                        |
|                                                    | 下单后初步检查              | ${opa}                        | ${user_code}                                         | ${billid}                                  |
|                                                    | ${pay_order}=               | 数据库查询                    | pay@tb_kernel_pay_order                              | sale_sys_orderid=${billid}                 |
|                                                    | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.pay_amount}                              |
|                                                    | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.order_cash}                              |
|                                                    | Should Be Equal As Integers | ${pay_order.pay_status}       | 1                                                    |
|                                                    | Should Be Equal             | ${pay_order.out_order_id}     | ${opa.oflinkid}                                      |
|                                                    | ${new_balance}=             | 获取用户信用点余额            | ${user_code}                                         |
|                                                    | log                         | ${new_balance.curr_balance}   |
|                                                    | Should Be Equal As Numbers  | ${new_balance.curr_balance}   | ${0}
|                                                    | ${where_cond}=              | create list                   | acct_id=${account_hff.acct_id}                       | sale_sys_orderid=${billid}                 |
|                                                    | ${balance_order}=           | 数据库查询                    | pay@tb_kernel_blc_order                              | ${where_cond}                              |
|                                                    | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${balance_order.pay_cash}                            |
|                                                    | Should Be Equal As Numbers  | ${new_balance.curr_balance}   | ${balance_order.left_balance}                        |
|                                                    | Should Be Equal As Integers | ${balance_order.pay_status}   | 1                                                    |
|                                                    | Should Be Equal As Strings  | ${balance_order.acct_id}      | ${account_hff.acct_id}                               |
|                                                    | Should Be Equal As Strings  | ${balance_order.acct_type_id} | ${ACCOUNT_TYPE_HFF}                                  |
|                                                    | ${where_cond}=              | create list                   | acct_id=${account_hff.acct_id}                       | sale_sys_orderid=${billid}                 |
|                                                    | @{settle_detail}=           | 数据库查询多行记录            | pay@tb_kernel_settle_detail                          | ${where_cond}                              |
|                                                    | :FOR                        | ${detail}                     | IN                                                   | @{settle_detail}                           |
|                                                    |                             | Run Keyword If                | ${detail.occur_type} ==${OCCUR_TYPE_TK}              | 校验退款余额明细                           | ${salebilltable} | ${0} | ${detail} | ${ACCOUNT_TYPE_HFF} |
|                                                    |                             | Run Keyword If                | ${detail.occur_type} ==${OCCUR_TYPE_XF}              | 校验支付成功余额明细                       | ${salebilltable} | ${0} | ${detail} | ${ACCOUNT_TYPE_HFF} |

| 信用点和后付费帐号都有，信用点余额充足，但后付费优先的商户下单 |
|                                                                | [Setup]                     | 校验用户的帐务信息            | ${OPA_PARAMS_USER_ALL_HFF_IS_FIRST_USE_HFF['userid']} |
|                                                                | Set Test Variable           | ${user_code}                  | ${OPA_PARAMS_USER_ALL_HFF_IS_FIRST_USE_HFF['userid']} |
|                                                                | 校验用户拥有两个可用帐号    | ${user_code}                  | ${False}                                               |
|                                                                | ${old_balance}=             | 获取用户信用点余额            | ${user_code}                                          |
|                                                                | log                         | ${old_balance.curr_balance}   |
|                                                                | ${opa}=                     | 大接口标准版本自定义参数下单  | onlineorder.do                                        | ${OPA_PARAMS_USER_ALL_HFF_IS_FIRST_USE_HFF} |
|                                                                | Set Test Variable           | ${billid}                     | ${opa.billid}                                         |
|                                                                | 下单后初步检查              | ${opa}                        | ${user_code}                                          | ${billid}                                   |
|                                                                | ${pay_order}=               | 数据库查询                    | pay@tb_kernel_pay_order                               | sale_sys_orderid=${billid}                  |
|                                                                | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.pay_amount}                               |
|                                                                | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${pay_order.order_cash}                               |
|                                                                | Should Be Equal As Integers | ${pay_order.pay_status}       | 1                                                     |
|                                                                | Should Be Equal             | ${pay_order.out_order_id}     | ${opa.oflinkid}                                       |
|                                                                | ${new_balance}=             | 获取用户信用点余额            | ${user_code}                                          |
|                                                                | log                         | ${new_balance.curr_balance}   |
|                                                                | ${where_cond}=              | create list                   | acct_id=${account_hff.acct_id}                        | sale_sys_orderid=${billid}                  |
|                                                                | ${balance_order}=           | 数据库查询                    | pay@tb_kernel_blc_order                               | ${where_cond}                               |
|                                                                | Should Be Equal As Numbers  | ${salebilltable.cash}         | ${balance_order.pay_cash}                             |
|                                                                | Should Be Equal As Numbers  | ${0}                          | ${balance_order.left_balance}                         |
|                                                                | Should Be Equal As Integers | ${balance_order.pay_status}   | 1                                                     |
|                                                                | Should Be Equal As Strings  | ${balance_order.acct_id}      | ${account_hff.acct_id}                                |
|                                                                | Should Be Equal As Strings  | ${balance_order.acct_type_id} | ${ACCOUNT_TYPE_HFF}                                   |
|                                                                | ${where_cond}=              | create list                   | acct_id=${account_hff.acct_id}                        | sale_sys_orderid=${billid}                  |
|                                                                | @{settle_detail}=           | 数据库查询多行记录            | pay@tb_kernel_settle_detail                           | ${where_cond}                               |
|                                                                | :FOR                        | ${detail}                     | IN                                                    | @{settle_detail}                            |
|                                                                |                             | Run Keyword If                | ${detail.occur_type} ==${OCCUR_TYPE_TK}               | 校验退款余额明细                            | ${salebilltable} | ${0} | ${detail} | ${ACCOUNT_TYPE_HFF} |
|                                                                |                             | Run Keyword If                | ${detail.occur_type} ==${OCCUR_TYPE_XF}               | 校验支付成功余额明细                        | ${salebilltable} | ${0} | ${detail} | ${ACCOUNT_TYPE_HFF} |

*** Keywords *** 
| 获取用户信用点余额 |
|                    | [Documentation] | 得到用户的信用点余额 |
|                    | [Arguments]     | ${user_code}         |
|                    | Comment         | 因为一个用户可能有   | 多个帐本，所以这次查询 | 加上预付费这个条件，这样就唯一了 |
|                    | ${where_cond}=  | create list          | user_code=${user_code} | acct_type_id=${ACCOUNT_TYPE_XYD} |
|                    | ${account}=     | 数据库查询           | pay@tb_kernel_account  | ${where_cond}                    |
|                    | ${balance}=     | 数据库查询           | pay@tb_kernel_balance  | acct_id=${account.acct_id}       |
|                    | [Return]        | ${balance}           |

| 校验用户拥有两个可用帐号 |
|                          | [Documentation]             | 校验用户拥有信用点和后付费两个帐号 | 并用都可用                                            | 也一并检查它们的优先级           |
|                          | [Arguments]                 | ${user_code}                       | ${xyd_is_first}                                       |
|                          | ${where_cond}=              | create list                        | user_code=${user_code}                                | acct_type_id=${ACCOUNT_TYPE_XYD} |
|                          | ${rec_xyd}=                 | 数据库查询                         | pay@tb_kernel_account                                 | ${where_cond}                    |
|                          | Set Test Variable           | ${account_xyd}                     | ${rec_xyd}
|                          | Should Be Equal As Integers | ${rec_xyd.data_status}             | 1                                                     |
|                          | Should Be Equal As Integers | ${rec_xyd.lock_status}             | 0                                                     |
|                          | ${where_cond}=              | create list                        | user_code=${user_code}                                | acct_type_id=${ACCOUNT_TYPE_HFF} |
|                          | ${rec_hff}=                 | 数据库查询                         | pay@tb_kernel_account                                 | ${where_cond}                    |
|                          | Set Test Variable           | ${account_hff}                     | ${rec_hff}
|                          | Should Be Equal As Integers | ${rec_hff.data_status}             | 1                                                     |
|                          | Should Be Equal As Integers | ${rec_hff.lock_status}             | 0                                                     |
|                          | ${real_priority}=           | Evaluate                           | ${rec_xyd.order_position} > ${rec_hff.order_position} |
|                          | Should Be Equal             | ${real_priority}                   | ${xyd_is_first}                                       |

| 校验用户的帐务信息 |
|                    | [Documentation]            | 检查用户在帐务侧是否具备下单的类目权限 |
|                    | [Arguments]                | ${user_code}                           |
|                    | ${rec}=                    | 数据库查询                             | pay@tb_kernel_merchant   | user_code=${user_code} |
|                    | comment                    | 设置user以防用例中需要用到             |
|                    | Should Be Equal AS Strings | ${rec.user_status}                     | 1                        |
|                    | Should Be Equal AS Strings | ${rec.data_status}                     | 1                        |
|                    | Should Be Equal AS Strings | ${rec.lock_status}                     | 0                        |
|                    | ${where_cond}=             | create list                            | cate_id=${HFKC_CATE_ID}  | user_code=${user_code} |
|                    | ${has_permission}=         | 数据库中记录是否存在                   | pay@tb_kernel_accountuse | ${where_cond}          |
|                    | Should Be True             | ${has_permission}                      |


| 下单后初步检查 |
|                | [Documentation]       | 下单后大致检查响应，销售订单表，充值表，帐务订单表 |
|                | [Arguments]           | ${opa}                                             | ${user_code}                 | ${billid}              |
|                | log                   | ${opa.resp_text}                                   |
|                | log                   | ${billid}                                          |
|                | ${verify_result}=     | 验证大接口标准版本下单响应                         | ${opa.resp_text}             | //retcode              | 1         | //sporder_id     | ${opa.oflinkid}    | //orderid | ${billid} |
|                | Should Be True        | ${verify_result}                                   |
|                | ${where_cond}=        | create list                                        | oflinkid=${opa.oflinkid}     | usercode=${user_code}  |
|                | ${rec}=               | 数据库查询                                         | main@salebilltable           | ${where_cond}          |
|                | Batch Should Be Equal | ${rec.billstat}                                    | ${billstate_payed}           | ${rec.billid}          | ${billid} | ${rec.gamecount} | ${opa.game_userid} |
|                | Set Test Variable     | ${salebilltable}                                   | ${rec}                       |
# |                | ${where_cond}=        | create list                                        | outorderid=${billid}         | add_m_no=${user_code}  |
# |                | ${is_exist}=          | 数据库中记录是否存在                               | ofrc@t_sys_orders            | ${where_cond}          |
# |                | Should Be True        | ${is_exist}                                        |
|                | ${where_cond}=        | create list                                        | out_order_id=${opa.oflinkid} | user_code=${user_code} |
|                | ${is_exist}=          | 数据库中记录是否存在                               | pay@tb_kernel_pay_order      | ${where_cond}          |
|                | Should Be True        | ${is_exist}                                        |

| 校验支付成功余额明细 |
|                      | [Documentation]            | 检查支付成功后余额明细表 |
|                      | [Arguments]                | ${salebilltable}         | ${balance_value}              | ${detail} | ${account_type_id} |
|                      | Should Be Equal As Numbers | ${balance_value}         | ${detail.left_balance}        |
|                      | ${value}=                  | Evaluate                 | -1000 * ${salebilltable.cash} |
|                      | Should Be Equal As Numbers | ${value}                 | ${detail.balance}             |
|                      | ${value}=                  | Evaluate                 | 1000 * ${salebilltable.cash}  |
|                      | Should Be Equal AS Numbers | ${value}                 | ${detail.expenditure_cost}    |
|                      | Should Be Equal            | ${detail.income_cost}    | ${None}                       |
|                      | Should Be Equal AS Strings | ${detail.occur_type}     | ${OCCUR_TYPE_XF}              |
|                      | Should Be Equal AS Strings | ${detail.payment_type}   | ${PAYMENT_TYPE_OUT}           |
|                      | Should Be Equal As Strings | ${detail.acct_type_id}   | ${account_type_id}            |

| 校验退款余额明细 |
|                  | [Documentation]            | 检查退款成功后余额明细表   |
|                  | [Arguments]                | ${salebilltable}           | ${balance_value}             | ${detail} | ${account_type_id} |
|                  | Should Be Equal As Numbers | ${balance_value}           | ${detail.left_balance}       |
|                  | ${value}=                  | Evaluate                   | 1000 * ${salebilltable.cash} |
|                  | Should Be Equal As Numbers | ${value}                   | ${detail.balance}            |
|                  | Should Be Equal AS Numbers | ${value}                   | ${detail.income_cost}        |
|                  | Should Be Equal            | ${detail.expenditure_cost} | ${None}                      |
|                  | Should Be Equal AS Strings | ${detail.occur_type}       | ${OCCUR_TYPE_TK}             |
|                  | Should Be Equal AS Strings | ${detail.payment_type}     | ${PAYMENT_TYPE_IN}           |
|                  | Should Be Equal As Strings | ${detail.acct_type_id}     | ${account_type_id}           |

# vim: set ft=robot ai et nu ts=4 sw=4 tw=240:
