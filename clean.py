import sys
import getopt
import gzip
from classes import ConData, file_to_con_data, LegData, hist_num_to_string_with_zero, Leg

def clean(argv):
    # default parameters
    max_clean_distance = 10000000
    min_clean_count = 4
    max_leg_distance = 1000
    max_leg_count = 10
    
    # progress display parameters
    display_max_num_legs = 20
    display_num_cons = 10000
    
    # read arguments
    try:
        opts, args = getopt.getopt(argv[1:], "d:c:D:C:R")
    except getopt.GetoptError as err:
        sys.stderr.write("[E::" + __name__ + "] unknown command\n")
        return 1
    if len(args) == 0:
        sys.stderr.write("Usage: metac clean [options] <in.con>\n")
        sys.stderr.write("Options:\n")
        sys.stderr.write("  -d INT     max distance (bp, L-1/2 norm) for removing isolated contacts [" + str(max_clean_distance) + "]\n")
        sys.stderr.write("  -c INT     min neighbor count for an unisolated contact [" + str(min_clean_count) + "]\n")
        sys.stderr.write("  -D INT     max distance (bp) for removing promiscuous legs [" + str(max_leg_distance) + "]\n")
        sys.stderr.write("  -C INT     max neighbor count for a nonpromiscuous leg [" + str(max_leg_count) + "]\n")
        return 1
    for o, a in opts:
        if o == "-d":
            max_clean_distance = int(a)
        elif o == "-c":
            min_clean_count = int(a)
        elif o == "-D":
            max_leg_distance = int(a)
        elif o == "-C":
            max_leg_count = int(a)
                     
    # read CON file
    con_file = gzip.open(args[0], "rb") if args[0].endswith(".gz") else open(args[0], "rb")
    con_data = file_to_con_data(con_file)
    original_num_cons = con_data.num_cons()
    sys.stderr.write("[M::" + __name__ + "] read " + str(con_data.num_cons()) + " putative contacts (" + str(round(100.0 * con_data.num_intra_chr() / con_data.num_cons(), 2)) + "% intra-chromosomal, " + str(round(100.0 * con_data.num_phased_legs() / con_data.num_cons() / 2, 2)) + "% legs phased)\n")
    #sys.stdout.write(con_data.to_string() + "\n")
    
    # pass 1: remove contacts containing promiscuous legs
    leg_data = LegData()
    leg_data.add_con_data(con_data)
    leg_data.sort_legs()
    sys.stderr.write("[M::" + __name__ + "] pass 1: sorted " + str(leg_data.num_legs()) + " legs\n")
    con_data.clean_promiscuous(leg_data, max_leg_distance, max_leg_count)
    pass_1_num_cons = con_data.num_cons()
    sys.stderr.write("[M::" + __name__ + "] pass 1 done: removed " + str(original_num_cons - pass_1_num_cons) + " contacts (" + str(round(100.0 - 100.0 * pass_1_num_cons / original_num_cons, 2)) + "%)\n")
    
    # pass 2: remove isolated contacts
    
    #sys.stderr.write("[M::" + __name__ + "] writing output for " + str(con_data.num_cons()) + " putative contacts (" + str(round(100.0 * con_data.num_intra_chr() / con_data.num_cons(), 2)) + "% intra-chromosomal, " + str(round(100.0 * con_data.num_phased_legs() / con_data.num_cons() / 2, 2)) + "% legs phased)\n")
    #sys.stdout.write(con_data.to_string()+"\n")
    
    return 0
    