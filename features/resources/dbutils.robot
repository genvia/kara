*** Settings ***
Documentation     据库操作相关的关键字
...               Author Pangdinghai
...               Version 0.0.1
Library           Collections
Library           kararfsclient.KaraLibs

*** Variables ***
${TRANSACTION_FLAG}    HANDLE_TRANSACTION

*** Keywords ***
数据库查询
    [Arguments]    ${dbname_and_table}    @{args}
    [Documentation]    从数据库中一个表查询返回单行记录
    ${recs}=    Fetch From Database Single Table    ${dbname_and_table}    @{args}
    [Return]    ${recs}

数据库查询多行记录
    [Arguments]    ${dbname_and_table}    @{args}
    [Documentation]    从数据库中一个表查询返回多行记录
    ${recs}=    Fetch Multi From Database Single Table    ${dbname_and_table}    @{args}
    [Return]    ${recs}

数据库插入
    [Arguments]    ${dbname_and_table}    ${kwargs}
    [Documentation]    向数据库一个表中插入记录
    ...    返回的是ResultProxy对象
    ${cur}=    Insert Into Database    ${dbname_and_table}    &{kwargs}
    [Return]    ${cur}

数据库删除
    [Arguments]    ${dbname_and_table}    ${where_cond}
    [Documentation]    从数据库一个表中删除记录
    ...    返回的是ResultProxy对象
    ${cur}=    Delete from Database    ${dbname_and_table}    ${where_cond}
    [Return]    ${cur}

数据库更新
    [Arguments]    ${dbname_and_table}    ${where_cond}    ${kwargs}
    [Documentation]    在数据库一个表中更新记录
    ...    返回的是ResultProxy对象
    ${cur}=    Update In database    ${dbname_and_table}    ${where_cond}    &{kwargs}
    [Return]    ${cur}

数据库执行SQL语句
    [Arguments]    ${dbname_and_table}    ${sql_statement}    &{kwargs}
    [Documentation]    在数据库中执行一个SQL语句
    ...    返回的是ResultProxy对象 可以支持额外的绑定参数
    ${cur}=    Execute Single Sql Statement    ${dbname_and_table}    ${sql_statement}    &{kwargs}
    [Return]    ${cur}

数据库执行SQL文件
    [Arguments]    ${dbname_and_table}    ${sql_file_name}    &{kwargs}
    [Documentation]    在数据库中同一个事务里执行一个SQL文件
    ...    返回的是Dictionary key是各SQL语句 value是本SQL语句影响的行数
    ...    可以支持额外的绑定参数
    ${dic}=    Execute Sql File    ${dbname_and_table}    ${sql_file_name}    &{kwargs}
    [Return]    ${dic}

数据库中记录是否存在
    [Arguments]    ${dbname_and_table}    @{where_conds}
    [Documentation]    检查数据库中记录是否存在
    ...    记录存在返回True，否则返回False
    ${recs}=    Fetch From Database Single Table    ${dbname_and_table}    @{where_conds}    count(*) as CNT
    ${is_exist}=    Convert To Boolean    ${recs.cnt}
    [Return]    ${is_exist}

数据库中记录条数
    [Arguments]    ${dbname_and_table}    @{where_conds}
    [Documentation]    查询数据库中记录的条数，然后返回
    ${recs}=    Fetch From Database Single Table    ${dbname_and_table}    @{where_conds}    count(*) as CNT
    ${result_count}=    Convert To Integer    ${recs.cnt}
    [Return]    ${result_count}

数据库事务开启
    [Arguments]    @{dabase_name_string}
    [Documentation]    数据库开启事务，参数是多个或一个数据库名称，例如：ofrc或main等
    ...    会在当前用例上下文设置一个用例级别的列表变量，名称固定为__transactions__, 一定不能覆盖它
    ...    事务开启后，必须显式的回滚或提交它们！
    Database Start Transaction    @{dabase_name_string}
    Set Tags    ${TRANSACTION_FLAG}

数据库事务提交
    [Documentation]    数据库提交事务
    ...    为了防止参数少传或漏传，故意不用参数，只会提交刚才开启的所有事务
    Database Commit Transaction

数据库事务回滚
    [Documentation]    数据库回滚事务
    ...    为了防止参数少传或漏传，故意不用参数，只会提交刚才开启的所有事务
    Database Rollback Transaction
    # vim: set ft=robot ai et nu ts=4 sw=4 tw=240:
