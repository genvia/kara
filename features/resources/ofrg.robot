*** Settings ***
| Documentation | 充值中心相关操作的关键字                               |
|               | ...                                                    | Author  | Pangdinghai |
|               | ...                                                    | Version | 0.0.1       |
| Library       | kararfsclient.KaraLibs                                 |
| Resource      | %{KARA_HOME}${/}features${/}resources${/}common.robot  |
| Resource      | %{KARA_HOME}${/}features${/}resources${/}dbutils.robot |


*** Variables *** 
| ${ofrg_state_11} | ${11}  |
| ${ofrg_state_12} | ${12}  |
| ${ofrg_state_13} | ${13}  |
| ${ofrg_state_14} | ${14}  |
| ${ofrg_state_15} | ${15}  |
| ${ofrg_state_16} | ${16}  |

*** Keywords *** 
| 供货商取单 |
|            | [Documentation]             | 充值中心，直充供货商取单   |
|            | [Arguments]                 | ${supuid}                  | ${num}=1  |
|            | ${ofrg_fetch}=              | Ofrg Fetch Order           | ${supuid} | ${num} |
|            | Should be Equal As Integers | ${ofrg_fetch.count}        | ${num}    |
|            | Should be True              | ${ofrg_fetch.real_success} |
|            | sleep                       | ${DELAY_TIME}              |
|            | [Return]                    | ${ofrg_fetch}              |

| 供货商回调成功 |
|                | [Documentation]  | 充值中心回调成功           |
|                | [Arguments]      | ${supuid}                  | ${billid} |
|                | ${ofrg_callback} | Ofrg Callback Order        | ${supuid} | ${billid} | successOrder |
|                | Should be Equal  | ${ofrg_callback.resp_text} | success   |
|                | sleep            | ${DELAY_TIME}              |
|                | [Return]         | ${ofrg_callback}           |

| 供货商回调撤销 |
|                | [Documentation]  | 充值中心回调撤销           |
|                | [Arguments]      | ${supuid}                  | ${billid} |
|                | ${ofrg_callback} | Ofrg Callback Order        | ${supuid} | ${billid} | cancelOrder |
|                | Should be Equal  | ${ofrg_callback.resp_text} | success   |
|                | sleep            | ${DELAY_TIME}              |
|                | [Return]         | ${ofrg_callback}           |

| 供货商回调可疑 |
|                | [Documentation]  | 充值中心回调可疑           |
|                | [Arguments]      | ${supuid}                  | ${billid} |
|                | ${ofrg_callback} | Ofrg Callback Order        | ${supuid} | ${billid} | unKnownReturn |
|                | Should be Equal  | ${ofrg_callback.resp_text} | success   |
|                | sleep            | ${DELAY_TIME}              |
|                | [Return]         | ${ofrg_callback}           |

| 供货商回调失败 |
|                | [Documentation]  | 充值中心回调失败           |
|                | [Arguments]      | ${supuid}                  | ${billid} |
|                | ${ofrg_callback} | Ofrg Callback Order        | ${supuid} | ${billid} | againOrder |
|                | Should be Equal  | ${ofrg_callback.resp_text} | success   |
|                | sleep            | ${DELAY_TIME}              |
|                | [Return]         | ${ofrg_callback}           |

| 重置订单表中数据的状态 |
|                        | [Documentation] | 把订单表中的订单状态置为起始测试状态 |
|                        | [Arguments]     | ${system_tbl}                        | ${recharg_tbl}                                 | ${start_days} |
|                        | ${where_cond}=  | Create list                          | order_time > trunc(sysdate-${start_days},'dd') | state=11      |
|                        | &{dict}=        | Create Dictionary                    | state=16                                       |
|                        | ${rec}=         | 数据库更新                           | ofrcmain@${system_tbl}                         | ${where_cond} | ${dict} |
|                        | ${rec}=         | 数据库更新                           | ofrcmain@${recharg_tbl}                        | ${where_cond} | ${dict} |
|

# vim: set ft=robot ai et nu ts=4 sw=4 tw=240:
