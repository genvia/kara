*** Settings ***
| Documentation | 通用的资源文件，主要为了扩充或封装 | 一些Robob framework自身或第三方通用的关键字 |
|               | ...                                | Author                                      | Pangdinghai |
|               | ...                                | Version                                     | 0.0.1       |
| Library       | String                             |


*** Variables *** 
| ${DELAY_TIME} | ${GLOBAL_DELAY} |


*** Keywords *** 
| Batch Should Be Equal |
|                       | [Documentation] | batch run Should's keyword |
|                       | [Arguments]     | @{args}                    |
|                       | ${div_by_2}=    | Evaluate                   | len(${args}) % 2 |
|                       | Should Be True  | ${0} == ${div_by_2}        |
|                       | :FOR            | ${first}                   | ${second}        | IN        | @{args} |
|                       |                 | Should Be Equal            | ${first}         | ${second} |

| Simple Delay |
|              | [Documentation] | Simple Delay using sleep  |
|              | ...             | default retry times is 2, | unit is 0.5s |
|              | [Arguments]     | ${retry}=2                |
|              | Repeat Keyword  | ${retry}                  | sleep        | 0.5s |
|              | [Return]        | True                      |

| Sub Element From String |
|                         | [Documentation] | get one element from delimited string |
|                         | [Arguments]     | ${str}                                | ${delimit_char}=,     | ${which}=${0}   |
|                         | @{elements}=    | Split String                          | ${str}                | ${delimit_char} |
|                         | ${element}=     | Strip String                          | ${elements[${which}]} |
|                         | [Return]        | ${element}                            |

# vim: set ft=robot ai et nu ts=4 sw=4 tw=240:

