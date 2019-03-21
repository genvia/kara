-- SQL file for kara Database object require:
--   1. one sql statement must completely be in one line.
--   2. can comment use '--' or '#', but have to comment at first column
--   3. ';' at end of one line is optional.
--   4. empty line is ignored.
--   5. file encoding must be utf-8

# change ofrc@t_sys_orders orders state
UPDATE t_sys_orders SET state=15 WHERE addtime>trunc(sysdate,'dd');

-- change ofrc@t_sys_orders orders state
UPDATE t_recharge_order SET state=14 WHERE addtime>trunc(sysdate,'dd');
