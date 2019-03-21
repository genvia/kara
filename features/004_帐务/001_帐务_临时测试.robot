*** Settings ***
| Metadata     | Version                                                     | 0.01              |
| Metadata     | Author                                                      | pangdinghai       |
| Metadata     | Running Id                                                  | ${KARA_CLIENT_ID} |
| Resource     | %{KARA_HOME}${/}features${/}resources${/}common.robot       |
| Resource     | %{KARA_HOME}${/}features${/}resources${/}dbutils.robot      |
| Resource     | %{KARA_HOME}${/}features${/}resources${/}kernel.robot       |
| Variables    | %{KARA_HOME}${/}features${/}variables${/}kernel_olp_user.py |
| Variables    | %{KARA_HOME}${/}features${/}variables${/}kernel_customize_vars.py |
| Default tags | 帐务                                                        |


*** Variables ***
| &{KERNER_PARAMS_OLP} | path=pay/paymentOlp | file=kernel_pay_olp.template.py |
| &{CUSTOM_ORDERID} | saleOrderId=str(S123456789088483721) |


*** Test Cases ***
| 帐务下Olp订单 |
|               | ${kernel}= | 帐务下单             | ${KERNER_PARAMS_OLP} |
|               | log        | ${kernel.payOrderId} |

| 帐务用自定义数据下Olp订单 |
|                           | ${kernel}= | 帐务下单             | ${OLP_USER_LOCKED} |
|                           | log        | ${kernel.payOrderId} |

| 帐务用自定义数据下Olp订单2 |
|                           | ${KERNEL_CUSTOMIZED_VARIABLES_OLP.extra_param}=  |  Set Variable  |  ${CUSTOM_ORDERID}  |
|                           | ${kernel}= | 帐务下单              | ${KERNEL_CUSTOMIZED_VARIABLES_OLP.fetch()} |
|                           | log        | ${kernel.payOrderId} |
