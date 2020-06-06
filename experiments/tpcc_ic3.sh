cd ../
rm outputs/stats.json
cp -r config-tpcc-std.h config.h

## algorithm
alg=BAMBOO
latch=LH_SPINLOCK
latch=LH_MCSLOCK
# [WW]
ww_starv_free="false"
# [BAMBOO]
dynamic="true"
retire="true"
cs_pf="false"
opt_raw="false"

## workload
wl="TPCC"
wh=2
perc=0.5 # payment percentage
user_abort="false"
com="true"
com_latch="false"

#other
threads=8
profile="true"
cnt=100000
penalty=50000

for i in 0 1 2 3 4
do
for com_latch in true
do
for alg in BAMBOO #SILO WOUND_WAIT WAIT_DIE NO_WAIT
do
for threads in 1 2 4 8 16 32
do
for wh in 1 2 4 8 16 32
do
timeout 100 python test.py CC_ALG=$alg LATCH=${latch} WW_STARV_FREE=${ww_starv_free} DYNAMIC_TS=$dynamic RETIRE_ON=$retire DEBUG_CS_PROFILING=${cs_pf} BB_OPT_RAW=${opt_raw} WORKLOAD=${wl} NUM_WH=${wh} PERC_PAYMENT=$perc TPCC_USER_ABORT=${user_abort} COMMUTATIVE_OPS=$com COMMUTATIVE_LATCH=${com_latch} THREAD_CNT=$threads DEBUG_PROFILING=${profile} MAX_TXN_PER_PART=$cnt ABORT_PENALTY=$penalty
done
done
done
done
done
#

cd outputs/
python3 collect_stats.py
mv stats.csv tpcc_com_latch_more.csv
mv stats.json tpcc_com_latch_more.json
cd ..

cd experiments/
python3 send_email.py tpcc_com_latch