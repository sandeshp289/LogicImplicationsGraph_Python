# LogicImplicationsGraph_Python

Description:

    Static Logic Implications in Python

Code I:

    Files:

        implications.py               : Python code
    
        s1423.lev                     : Input circuit file (for e.g. s1423) in lev format

        s1423.impl                    : Output file (containing implications for all gates)

        s1423_5.impl                  : Output file (containing implications for gate 5)

    Execution:

        python implications.py s1423 node_number/all


Code II:

    Files:
        implications_flops_csv.py     : Python code
    
        s1423.lev                     : Input circuit file (for e.g. s1423) in lev format

        s1423_yes.impl                : Output file (containing implications for all flip-flops, considering PI/PO implications)

        s1423_yes.csv                 : Output file (CSV file to use for ML, considering PI/PO implications)
        
        s1423_no.impl                 : Output file (containing implications for all flip-flops, without considering PI/PO implications)

        s1423_no.csv                  : Output file (CSV file to use for ML, without considering PI/PO implications)
        
    
    Execution:

        python implications_flops_csv.py s1423 yes/no

