cp -r config-ycsb-std.h config.h

# algorithm
alg=$1
latch=LH_MCSLOCK
# [WW]
ww_starv_free="false"
# [BAMBOO]
dynamic="true"
retire_on="true"
cs_pf="false"
opt_raw=$2

# workload
wl="YCSB"
req=16
synthetic=false
zipf=0.99
num_hs=0
pos=TOP
specified=0
fixed=1
fhs="WR"
shs="WR"
read_ratio=0.9
ordered="false"
flip=0
table_size="1000000"

# other
threads=16
profile="true"
cnt=100000
penalty=50000

# temp settings
#dynamic="false"
#read_ratio=0.01
#table_size="1024*10"

python test_debug.py CC_ALG=${alg} LATCH=${latch} WW_STARV_FREE=${ww_starv_free} DYNAMIC_TS=${dynamic} RETIRE_ON=${retire_on} DEBUG_CS_PROFILING=${cs_pf} BB_OPT_RAW=${opt_raw} WORKLOAD=${wl} REQ_PER_QUERY=$req SYNTHETIC_YCSB=$synthetic ZIPF_THETA=$zipf NUM_HS=${num_hs} POS_HS=$pos SPECIFIED_RATIO=${specified} FIXED_HS=${fixed} FIRST_HS=$fhs SECOND_HS=$shs READ_PERC=${read_ratio} KEY_ORDER=$ordered FLIP_RATIO=${flip} SYNTH_TABLE_SIZE=${table_size} THREAD_CNT=$threads DEBUG_PROFILING=$profile MAX_TXN_PER_PART=$cnt ABORT_PENALTY=$penalty
#