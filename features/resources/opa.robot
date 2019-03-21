*** Settings ***
| Documentation | 大接口标准版本相关的用户关键字                        |
|               | ...                                                   | Author  | Pangdinghai |
|               | ...                                                   | Version | 0.0.1       |
| Library       | kararfsclient.KaraLibs                                |
| Resource      | %{KARA_HOME}${/}features${/}resources${/}common.robot |


*** Variables *** 
| ${billstate_nopay}              | 0               |
| ${billstate_payed}              | 1               |
| ${already_success}              | 1               |
| ${already_cancel}               | 9               |
| ${already_underway}             | 0               |
| ${complete_success}             | ${1}            |
| ${complete_cancel}              | ${2}            |
| ${retcode_order_create_failure} | 331             |
| ${retcode_balance_not_enough}   | 1007            |


*** Keywords *** 
| 大接口标准版本下单 |
|                    | [Documentation] | 大接口标准版本下单，参数是订单的类型，例如HF               | LL CARD_PASS之类，下单参数从参数文件中自动得到 |
|                    | ...             | fetch_billid，如果是True，将会从下单后的xml中解析出billid  | 这一般是在预料到成功时才设为True，缺省为False  |
|                    | ...             | 如果传递了附加的接口参数，将会覆盖掉参数文件中同名的参数值 | 附加参数缺省为None                             |
|                    | [Arguments]     | ${order_type}                                              | ${fetch_billid}=${False}                       | ${extra_params}=${None} |
|                    | ${opa}=         | Opa Standard Make Order                                    | ${order_type}                                  | ${fetch_billid}         | ${extra_params} |
|                    | sleep           | ${DELAY_TIME}                                              |
|                    | [Return]        | ${opa}                                                     |

| 大接口标准版本自定义参数下单 |
|                              | [Documentation] | 大接口标准版本下单，所有的参数需要自行传入， | 类型为大接口的接口名称和一个所有参数的Dictionary | 以及一个要不要第一时间校验下单成功的标志 |
|                              | [Arguments]     | ${interface_path}                            | ${params}                                        | ${stricted}=${True}                      |
|                              | ${opa}=         | Opa Standard Make Order Using Dict           | ${interface_path}                                | ${params}                                | ${stricted} |
|                              | sleep           | ${DELAY_TIME}                                |
|                              | [Return]        | ${opa}                                       |

| 验证大接口标准版本下单响应 |
|                            | [Documentation]   | 大接口标准版本下单后，检查HTTP的响应内容 |
|                            | [Arguments]       | ${response_text}                         | @{conditins}     |
|                            | ${verify_result}= | Opa Standard Batch Validate              | ${response_text} | @{conditins} |
|                            | [Return]          | ${verify_result}                         |


# vim: set ft=robot nowrap ai et nu ts=4 sw=4 tw=240:
