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
| ${ACCOUNT_TYPE_YFF} | 01    |
| ${ACCOUNT_TYPE_HFF} | 02    |

*** Test Cases *** 
| 已经被废弃的商户下单 |
|                      | [Setup]                    | 查询用户的帐本信息           | ${OPA_PARAMS_USER_DISCARD['userid']} |
|                      | Should Be Equal AS Strings | ${user_info.user_status}     | 1                                    |
|                      | Should Be Equal AS Strings | ${user_info.data_status}     | 0                                    |
|                      | Should Be Equal AS Strings | ${user_info.lock_status}     | 0                                    |
|                      | ${opa}=                    | 大接口标准版本自定义参数下单 | onlineorder.do                       | ${OPA_PARAMS_USER_DISCARD} | ${False}                        |
|                      | ${verify_result}=          | 验证大接口标准版本下单响应   | ${opa.resp_text}                     | //retcode                  | ${retcode_order_create_failure} |
|                      | Should Be True             | ${verify_result}             |
|                      | ${where_cond}=             | create list                  | oflinkid=${opa.oflinkid}             | userid=${opa.userid}       |
|                      | ${is_exist}=               | 数据库中记录是否存在         | main@salebilltable                   | ${where_cond}              |
|                      | Should Not Be True         | ${is_exist}                  |
|                      | ${where_cond}=             | create list                  | out_order_id=${opa.oflinkid}         | user_code=${opa.userid}    |
|                      | ${is_exist}=               | 数据库中记录是否存在         | pay@tb_kernel_pay_order              | ${where_cond}              |
|                      | Should Not Be True         | ${is_exist}                  |

| 已经被锁定的商户下单 |
|                      | [Setup]                    | 查询用户的帐本信息           | ${OPA_PARAMS_USER_LOCKED['userid']} |
|                      | Should Be Equal AS Strings | ${user_info.user_status}     | 1                                   |
|                      | Should Be Equal AS Strings | ${user_info.data_status}     | 1                                   |
|                      | Should Be Equal AS Strings | ${user_info.lock_status}     | 1                                   |
|                      | ${opa}=                    | 大接口标准版本自定义参数下单 | onlineorder.do                      | ${OPA_PARAMS_USER_LOCKED} | ${False}                        | 
|                      | ${verify_result}=          | 验证大接口标准版本下单响应   | ${opa.resp_text}                    | //retcode                 | ${retcode_order_create_failure} |
|                      | Should Be True             | ${verify_result}             |
|                      | ${where_cond}=             | create list                  | oflinkid=${opa.oflinkid}            | userid=${opa.userid}      |
|                      | ${is_exist}=               | 数据库中记录是否存在         | main@salebilltable                  | ${where_cond}             |
|                      | Should Not Be True         | ${is_exist}                  |
|                      | ${where_cond}=             | create list                  | out_order_id=${opa.oflinkid}        | user_code=${opa.userid}   |
|                      | ${is_exist}=               | 数据库中记录是否存在         | pay@tb_kernel_pay_order             | ${where_cond}             |
|                      | Should Not Be True         | ${is_exist}                  |

| 仅有后付费帐号没有下单权限的商户下单 |
|                                      | [Setup]                    | 查询用户的帐本信息           | ${OPA_PARAMS_USER_CATEGORY_LIMITED['userid']} |
|                                      | Should Be Equal AS Strings | ${user_info.user_status}     | 1                                             |
|                                      | Should Be Equal AS Strings | ${user_info.data_status}     | 1                                             |
|                                      | Should Be Equal AS Strings | ${user_info.lock_status}     | 0                                             |
|                                      | ${where_cond}=             | create list                  | cate_id=${HFKC_CATE_ID}                       | user_code=${OPA_PARAMS_USER_CATEGORY_LIMITED['userid']} |
|                                      | ${has_permission}=         | 数据库中记录是否存在         | pay@tb_kernel_accountuse                      | ${where_cond}                                           |
|                                      | Should Not Be True         | ${has_permission}            |
|                                      | ${opa}=                    | 大接口标准版本自定义参数下单 | onlineorder.do                                | ${OPA_PARAMS_USER_CATEGORY_LIMITED}                     | ${False}                        | 
|                                      | log                        | ${opa.resp_text}             |
|                                      | ${verify_result}=          | 验证大接口标准版本下单响应   | ${opa.resp_text}                              | //retcode                                               | ${retcode_order_create_failure} |
|                                      | Should Be True             | ${verify_result}             |
|                                      | ${where_cond}=             | create list                  | oflinkid=${opa.oflinkid}                      | userid=${opa.userid}                                    |
|                                      | ${is_exist}=               | 数据库中记录是否存在         | main@salebilltable                            | ${where_cond}                                           |
|                                      | Should Not Be True         | ${is_exist}                  |
|                                      | ${where_cond}=             | create list                  | out_order_id=${opa.oflinkid}                  | user_code=${opa.userid}                                 |
|                                      | ${is_exist}=               | 数据库中记录是否存在         | pay@tb_kernel_pay_order                       | ${where_cond}                                           |
|                                      | Should Not Be True         | ${is_exist}                  |

| 信用点和后付费帐号都没有下单权限的商户下单 |
|                                            | [Setup]                    | 查询用户的帐本信息           | ${OPA_PARAMS_USER_ALL_CATEGORY_LIMITED['userid']} |
|                                            | Should Be Equal AS Strings | ${user_info.user_status}     | 1                                                 |
|                                            | Should Be Equal AS Strings | ${user_info.data_status}     | 1                                                 |
|                                            | Should Be Equal AS Strings | ${user_info.lock_status}     | 0                                                 |
|                                            | @{accounts}=               | 数据库查询多行记录           | pay@tb_kernel_account                             | user_code=${OPA_PARAMS_USER_ALL_CATEGORY_LIMITED['userid']} |
|                                            | :FOR                       | ${account}                   | IN                                                | @{accounts}                                                 |
|                                            |                            | log                          | ${account.acct_id}                                |
|                                            |                            | ${where_cond}=               | create list                                       | cate_id=${HFKC_CATE_ID}                                     | user_code=${OPA_PARAMS_USER_ALL_CATEGORY_LIMITED['userid']} |
|                                            |                            | ${has_permission}=           | 数据库中记录是否存在                              | pay@tb_kernel_accountuse                                    | ${where_cond}
|                                            |                            | Should Not Be True           | ${has_permission}                                 |
|                                            | ${opa}=                    | 大接口标准版本自定义参数下单 | onlineorder.do                                    | ${OPA_PARAMS_USER_ALL_CATEGORY_LIMITED}                     | ${False}                                                    | 
|                                            | log                        | ${opa.resp_text}             |
|                                            | ${verify_result}=          | 验证大接口标准版本下单响应   | ${opa.resp_text}                                  | //retcode                                                   | ${retcode_order_create_failure}                             |
|                                            | Should Be True             | ${verify_result}             |
|                                            | ${where_cond}=             | create list                  | oflinkid=${opa.oflinkid}                          | userid=${opa.userid}                                        |
|                                            | ${is_exist}=               | 数据库中记录是否存在         | main@salebilltable                                | ${where_cond}                                               |
|                                            | Should Not Be True         | ${is_exist}                  |
|                                            | ${where_cond}=             | create list                  | out_order_id=${opa.oflinkid}                      | user_code=${opa.userid}                                     |
|                                            | ${is_exist}=               | 数据库中记录是否存在         | pay@tb_kernel_pay_order                           | ${where_cond}                                               |
|                                            | Should Not Be True         | ${is_exist}                  |

| 信用点预付费用户余额不足时下单 |
|                                | [Setup]                    | 查询用户的帐本信息           | ${OPA_PARAMS_USER_BALANCE_IS_ZERO['userid']}           |
|                                | Should Be Equal AS Strings | ${user_info.user_status}     | 1                                                      |
|                                | Should Be Equal AS Strings | ${user_info.data_status}     | 1                                                      |
|                                | Should Be Equal AS Strings | ${user_info.lock_status}     | 0                                                      |
|                                | ${where_cond}=             | create list                  | user_code=${OPA_PARAMS_USER_BALANCE_IS_ZERO['userid']} |
|                                | ${account}=                | 数据库查询                   | pay@tb_kernel_account                                  | ${where_cond}                                          |
|                                | Comment                    | 数据库查询返回对象           | 如果用obj.propertye形式不出错就表明只有单条数据        | 所以此用户只有信用点                                   |
|                                | Should Be Equal AS Strings | ${account.acct_type_id}      | ${ACCOUNT_TYPE_YFF}                                    |
|                                | ${where_cond}=             | create list                  | cate_id=${HFKC_CATE_ID}                                | user_code=${OPA_PARAMS_USER_BALANCE_IS_ZERO['userid']} |
|                                | ${has_permission}=         | 数据库中记录是否存在         | pay@tb_kernel_accountuse                               | ${where_cond}                                          |
|                                | Should Be True             | ${has_permission}            |
|                                | ${opa}=                    | 大接口标准版本自定义参数下单 | onlineorder.do                                         | ${OPA_PARAMS_USER_BALANCE_IS_ZERO}                     | ${False}                      | 
|                                | log                        | ${opa.resp_text}             |
|                                | ${verify_result}=          | 验证大接口标准版本下单响应   | ${opa.resp_text}                                       | //retcode                                              | ${retcode_balance_not_enough} |
|                                | Should Be True             | ${verify_result}             |
|                                | ${where_cond}=             | create list                  | oflinkid=${opa.oflinkid}                               | userid=${opa.userid}                                   |
|                                | ${is_exist}=               | 数据库中记录是否存在         | main@salebilltable                                     | ${where_cond}                                          |
|                                | Should Not Be True         | ${is_exist}                  |
|                                | ${where_cond}=             | create list                  | out_order_id=${opa.oflinkid}                           | user_code=${opa.userid}                                |
|                                | ${is_exist}=               | 数据库中记录是否存在         | pay@tb_kernel_pay_order                                | ${where_cond}                                          |
|                                | Should Not Be True         | ${is_exist}                  |

*** Keywords *** 
| 查询用户的帐本信息 |
|                    | [Arguments]       | ${user_code} |
|                    | ${where_cond}=    | create list  | user_code=${user_code} |
|                    | ${rec}=           | 数据库查询   | pay@tb_kernel_merchant | ${where_cond} |
|                    | Set Test Variable | ${user_info} | ${rec}                 |

# vim: set ft=robot nowrap ai et nu ts=4 sw=4 tw=240:

