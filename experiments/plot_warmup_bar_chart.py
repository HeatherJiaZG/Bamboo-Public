import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import json


def getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, CC_ALG, dname, metric_name):
    '''
    return np.array
    '''
    resultsList, results_dict = [], {}
    filename = '/users/heatherj/fast_disk/Bamboo-Public/outputs/'+dname+'/'+dname+'_readperc'+str(READ_PERC)+'.json'

    # read json file
    with open(filename) as f:
        for jsonObj in f:
            resultDict = json.loads(jsonObj)
            resultsList.append(resultDict)

    # parse json
    for one_result in resultsList:
        if float(one_result["ZIPF_THETA"]) == ZIPF_THETA and float(one_result["READ_PERC"]) == READ_PERC and one_result["CC_ALG"] == CC_ALG:
            # metric_name: int(one_result[metric_name])
            # "THREAD_CNT"=int(one_result["THREAD_CNT"])
            results_dict[int(one_result["THREAD_CNT"])] = float(one_result[metric_name])
    # reorder results in ascending THREAD_CNT order
    results_ordered = []
    for thd_cnt in THREAD_CNT_list:
        results_ordered.append(results_dict[thd_cnt])
    # print("dname=",dname," ,",results_ordered)
    return np.array(results_ordered)


if __name__ == "__main__":
    THREAD_CNT_list = [1, 2, 4, 8, 16, 32]
    THREAD_CNT_nparray = np.array(THREAD_CNT_list)
    dname_non_warmup="ycsb_non_warmup_cache"
    dname_warmup="ycsb_warmup_cache"
    dname_warmup_txn="ycsb_warmup_cache_txn_commit_latency"
    metric_name = "decomposed_commit_latency" # throughput, commit_latency, decomposed_commit_latency
    plot_option = 2 # (1: for three curves. (2: for the decomposed_commit_latency
    barWidth = 0.25
    pic_num = 0

    for READ_PERC in [0.5]:
        for ZIPF_THETA in [0.9]: # [0.3, 0.5, 0.7, 0.9, 0.999]:
            fig = plt.figure(pic_num)
            pic_num += 1
            
            if plot_option == 1:
                # for three curves: nowait warm up, nowait not warm up, silo
                nowait_warmup_y = getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, "NO_WAIT", dname_warmup_txn, metric_name)
                nowait_nowarmup_y = getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, "NO_WAIT", dname_non_warmup, metric_name)
                silo_y = getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, "SILO", dname_non_warmup, metric_name)
                
                # Set position of bar on X axis
                br1 = np.arange(len(THREAD_CNT_list))
                br2 = [x + barWidth for x in br1]
                br3 = [x + barWidth for x in br2]
                # Make the plot
                plt.bar(br1, nowait_nowarmup_y, color ='r', width = barWidth, label ='nowait_nowarmup')
                plt.bar(br2, nowait_warmup_y, color ='g', width = barWidth, label ='nowait_warmup')
                plt.bar(br3, silo_y, color ='b', width = barWidth, label ='silo')
                # Adding Xticks
                plt.xlabel('THREAD_CNT', fontweight ='bold', fontsize = 8)
                plt.ylabel(metric_name, fontweight ='bold', fontsize = 8)
                plt.xticks([r + barWidth for r in range(len(THREAD_CNT_list))], THREAD_CNT_list)

            else:
                # for the decomposed_commit_latency
                nowait_warmup_txn_commit_latency_y = getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, "NO_WAIT", dname_warmup_txn, "warmed_up_commit_latency")
                nowait_nowarmup_txn_commit_latency_y = getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, "NO_WAIT", dname_warmup_txn, "unwarmed_up_commit_latency")

                # Set position of bar on X axis
                br1 = np.arange(len(THREAD_CNT_list))
                br2 = [x + barWidth for x in br1]
                # Make the plot
                plt.bar(br1, nowait_warmup_txn_commit_latency_y, color ='r', width = barWidth, label ='nowait_warmup')
                plt.bar(br2, nowait_nowarmup_txn_commit_latency_y, color ='g', width = barWidth, label ='nowait_nowarmup')
                # Adding Xticks
                plt.xlabel('THREAD_CNT', fontweight ='bold', fontsize = 8)
                plt.ylabel('decomposed_commit_latency', fontweight ='bold', fontsize = 8)
                plt.xticks([r + barWidth for r in range(len(THREAD_CNT_list))], THREAD_CNT_list)

                # print txn_cnt
                warmed_up_txn_cnt = getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, "NO_WAIT", dname_warmup_txn, "warmed_up_txn_cnt")
                unwarmed_up_txn_cnt = getResult(ZIPF_THETA, READ_PERC, THREAD_CNT_list, "NO_WAIT", dname_warmup_txn, "unwarmed_up_txn_cnt")
                print("READ_PERC=",str(READ_PERC),", ZIPF_THETA=",str(ZIPF_THETA))
                print("warmed_up_txn_cnt=",warmed_up_txn_cnt)
                print("unwarmed_up_txn_cnt=",unwarmed_up_txn_cnt)
                print("\n")


            plt.xlabel("THREAD_CNT")
            plt.ylabel(metric_name)
            plt.legend()
            plt.title('ZIPF_THETA='+str(ZIPF_THETA)+'\nREAD_PERC='+str(READ_PERC))
            plt.savefig('figures/'+metric_name+'/READ_PERC'+str(READ_PERC)+'-ZIPF_THETA'+str(ZIPF_THETA)+'_bar.png')
           

