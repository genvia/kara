*** Settings ***
| Metadata     | Version                                                 | 0.01        |
| Metadata     | Author                                                  | pangdinghai |
| Resource     | %{KARA_HOME}${/}features${/}resources${/}common.robot   |
| Resource     | %{KARA_HOME}${/}features${/}resources${/}dbutils.robot  |
| Resource     | %{KARA_HOME}${/}features${/}resources${/}opa.robot      |
| Variables    | %{KARA_HOME}${/}features${/}variables${/}opa_special.py |
| Default tags | temp                                                    | test        | robot  |


*** Test Cases *** 
| test temp  |
|            | log | ${KARA_CLIENT_ID} |
| test temp2 |
|            | log | ${KARA_CLIENT_ID} |

| test db transaction 1 |
|                       | [Setup]                     | 数据库事务开启     | main           | ofrc            |
|                       | [Teardown]                  | 数据库事务回滚     |
|                       | &{rec}=                     | Create Dictionary  | mid=pdh        | value=genvia    | key=inc010061 |
|                       | log                         | ${rec}             |
|                       | ${result}=                  | 数据库插入         | ofrc@mb_config | ${rec}          |
|                       | log                         | ${result.rowcount} |
|                       | Should Be Equal As Integers | ${result.rowcount} | ${1}           |
|                       | &{rec}=                     | Create Dictionary  | value=jmc      | key=of669       |
|                       | ${result}=                  | 数据库更新         | ofrc@mb_config | mid=pdh         | ${rec}        |
|                       | log                         | ${result.rowcount} |
|                       | Should Be Equal As Integers | ${result.rowcount} | ${1}           |
|                       | ${result}=                  | 数据库删除         | ofrc@mb_config | mid=pdh         |
|                       | Should Be Equal As Integers | ${result.rowcount} | ${1}           |
|                       | ${result}=                  | 数据库删除         | main@saleuser  | usercode=A08566 |
|                       | Should Be Equal As Integers | ${result.rowcount} | ${1}           |


| test db operate |
|                 | &{rec}=                     | Create Dictionary  | mid=pdh        | value=genvia | key=inc010061 |
|                 | log                         | ${rec}             |
|                 | ${result}=                  | 数据库插入         | ofrc@mb_config | ${rec}       |
|                 | log                         | ${result.rowcount} |
|                 | Should Be Equal As Integers | ${result.rowcount} | ${1}           |
|                 | &{rec}=                     | Create Dictionary  | value=jmc      | key=of669    |
|                 | ${result}=                  | 数据库更新         | ofrc@mb_config | mid=pdh      | ${rec}        |
|                 | log                         | ${result.rowcount} |
|                 | Should Be Equal As Integers | ${result.rowcount} | ${1}           |
|                 | ${result}=                  | 数据库删除         | ofrc@mb_config | mid=pdh      |
|                 | Should Be Equal As Integers | ${result.rowcount} | ${1}           |

